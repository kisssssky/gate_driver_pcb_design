#!/usr/bin/env python3
"""Reproducible G2 first-order electrical calculations.

This script intentionally does not claim device qualification.  Datasheet typical
values and explicitly bounded engineering assumptions are separated in the data
structures below.  Run with Python 3.10+; no third-party modules are required.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from math import log, sqrt
import argparse
import json


@dataclass(frozen=True)
class Dut:
    name: str
    qg_nc: float
    ciss_nf: float
    crss_pf: float
    coss_pf: float
    rg_int_ohm: float
    rds_on_ohm: float
    vth_min_v: float
    vth_typ_v: float
    vth_max_v: float
    source: str


@dataclass(frozen=True)
class RailCase:
    name: str
    high_v: float
    low_v: float
    transition: str

    @property
    def span_v(self) -> float:
        return self.high_v - self.low_v


DUTS = {
    "650V": Dut(
        "SCTW35N65G2VAG", 73.0, 1.370, 30.0, 125.0, 2.0, 0.055,
        1.8, 3.2, 5.0,
        "ST DS12885 Rev 3, Sep-2020, Tables 3-4",
    ),
    "3K3_PROXY": Dut(
        "DUT-PROXY-3K3-G2R50MT33K-3P-v0.1", 340.0, 7.302, 12.3,
        131.0, 1.2, 0.050, 2.0, 2.75, 3.5,
        "GeneSiC G2R50MT33K Rev 23/Jul, pp.1-2; 3-pin conversion is assumption",
    ),
}

RAILS = {
    "650V_P": RailCase("650V positive", 18.0, 4.0, "sink"),
    "650V_N": RailCase("650V negative", 4.0, -5.0, "source"),
    "3K3_P": RailCase("3.3kV proxy positive", 20.0, 3.0, "sink"),
    "3K3_N": RailCase("3.3kV proxy negative", 3.0, -5.0, "source"),
}

# Driver facts: Si8273 Table 8; UCC27614 Tables 6-5 and 6-6.
DRIVERS = {
    "SI8273_TYP": dict(rsrc=2.7, rsink=1.0, isrc=1.8, isink=4.0, tpd_ns=30.0),
    "SI8273_WC_TIMING": dict(rsrc=2.7, rsink=1.0, isrc=1.8, isink=4.0, tpd_ns=60.0),
    "UCC27614_TYP": dict(rsrc=2.5, rsink=0.34, isrc=10.0, isink=10.0, tpd_ns=17.5),
    "UCC27614_WC": dict(rsrc=4.5, rsink=0.55, isrc=10.0, isink=10.0, tpd_ns=27.0),
}


def qg_current_a(qg_nc: float, transition_ns: float) -> float:
    return qg_nc / transition_ns


def peak_current_a(delta_v: float, r_total: float, current_limit_a: float) -> float:
    return min(delta_v / r_total, current_limit_a)


def rc_10_90_ns(c_nf: float, r_ohm: float) -> float:
    return 2.2 * c_nf * r_ohm


def threshold_cross_ns(c_nf: float, r_ohm: float, v0: float, vf: float, vth: float) -> float:
    fraction = (vth - v0) / (vf - v0)
    if not 0.0 < fraction < 1.0:
        raise ValueError("threshold must lie between initial and final voltages")
    return -r_ohm * c_nf * log(1.0 - fraction)


def decoupling_uf(q_nc: float, droop_v: float, margin: float = 2.0) -> float:
    return margin * q_nc * 1e-3 / droop_v


def average_gate_current_ma(q_nc: float, rep_hz: float, edges_per_cycle: int = 2) -> float:
    return q_nc * 1e-6 * rep_hz * edges_per_cycle


def dynamic_gate_power_w(q_nc: float, rail_span_v: float, rep_hz: float) -> float:
    return q_nc * 1e-9 * rail_span_v * rep_hz


def rl_current_a(vdc_v: float, vds_v: float, rl_ohm: float) -> float:
    return (vdc_v - vds_v) / rl_ohm


def pulse_energy_j(vdc_v: float, current_a: float, pulse_s: float) -> float:
    return vdc_v * current_a * pulse_s


def bandwidth_mhz(edge_ns: float, accuracy_factor: float = 5.0) -> float:
    return accuracy_factor * 0.35 / (edge_ns * 1e-9) / 1e6


def sample_rate_gsa(edge_ns: float, samples_per_edge: int = 20) -> float:
    return samples_per_edge / (edge_ns * 1e-9) / 1e9


def rss_ns(*terms_ns: float) -> float:
    return sqrt(sum(x * x for x in terms_ns))


def gate_case(dut: Dut, rail: RailCase, rg: float, driver: dict,
              rloop: float = 0.2, lgate_nh: float = 10.0) -> dict:
    rout = driver["rsrc"] if rail.transition == "source" else driver["rsink"]
    ilimit = driver["isrc"] if rail.transition == "source" else driver["isink"]
    rtotal = rout + rg + dut.rg_int_ohm + rloop
    ipeak = peak_current_a(rail.span_v, rtotal, ilimit)
    return {
        "dut": dut.name,
        "rail": rail.name,
        "transition": rail.transition,
        "span_V": rail.span_v,
        "Rg_ohm": rg,
        "Rtotal_ohm": round(rtotal, 3),
        "Ipk_A": round(ipeak, 3),
        "Qg_over_100ns_A": round(qg_current_a(dut.qg_nc, 100.0), 3),
        "RC_10_90_ns": round(rc_10_90_ns(dut.ciss_nf, rtotal), 1),
        "Ldi_dt_V_at_Ipk_over_10ns": round(lgate_nh * ipeak / 10.0, 2),
    }


def report() -> dict:
    rg = {"650V": 1.0, "3K3_PROXY": 0.5}
    cases = []
    for profile, rail_keys in (("650V", ("650V_P", "650V_N")),
                               ("3K3_PROXY", ("3K3_P", "3K3_N"))):
        for key in rail_keys:
            cases.append(gate_case(DUTS[profile], RAILS[key], rg[profile],
                                   DRIVERS["UCC27614_TYP"]))

    decoupling = {}
    for key, dut in DUTS.items():
        decoupling[key] = {
            "Cmin_uF_at_0p5V_droop_2x": round(decoupling_uf(dut.qg_nc, 0.5), 3),
            "Iavg_mA_1kHz_two_edges": round(average_gate_current_ma(dut.qg_nc, 1000), 3),
        }

    timing = {
        "nominal_fixed_delay_ns": 30.0 + 17.5,
        "worst_case_fixed_delay_ns": 60.0 + 27.0,
        "uncertainty_rss_example_ns": round(rss_ns(1.0, 0.2, 1.0, 2.0, 3.0), 2),
        "note": "Gate/DUT/VDS/probe terms must be added from LTspice and G10/G11 measurement.",
    }
    measurement = {
        "for_10ns_edge_BW_MHz_5x": round(bandwidth_mhz(10.0), 1),
        "for_10ns_edge_sample_GSa_s_20pts": round(sample_rate_gsa(10.0), 1),
        "for_20ns_edge_BW_MHz_5x": round(bandwidth_mhz(20.0), 1),
        "for_20ns_edge_sample_GSa_s_20pts": round(sample_rate_gsa(20.0), 1),
    }
    drain_example = {
        "VDC_V": 10.0,
        "VDS_V": 2.0,
        "RL_ohm": 100.0,
        "IDS_A": round(rl_current_a(10.0, 2.0, 100.0), 3),
        "E_1us_uJ_upper_bound": round(pulse_energy_j(10.0, 0.08, 1e-6) * 1e6, 3),
        "status": "illustrative only; MI/MP/MN target current and approved RL remain open",
    }
    return {
        "evidence_boundary": "CALCULATION using DATASHEET FACT plus stated ENGINEERING ASSUMPTION",
        "duts": {k: asdict(v) for k, v in DUTS.items()},
        "gate_cases": cases,
        "decoupling": decoupling,
        "timing": timing,
        "measurement": measurement,
        "drain_example": drain_example,
    }


def self_check(data: dict) -> None:
    assert abs(qg_current_a(73.0, 100.0) - 0.73) < 1e-12
    assert abs(decoupling_uf(340.0, 0.5) - 1.36) < 1e-12
    assert abs(rl_current_a(10.0, 2.0, 100.0) - 0.08) < 1e-12
    assert len(data["gate_cases"]) == 4
    assert all(x["span_V"] >= 8.0 for x in data["gate_cases"])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--compact", action="store_true")
    args = parser.parse_args()
    data = report()
    self_check(data)
    print(json.dumps(data, indent=None if args.compact else 2, ensure_ascii=False))


if __name__ == "__main__":
    main()
