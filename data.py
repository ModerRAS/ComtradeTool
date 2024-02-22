直流场电流模拟量 = [
    "IDEL1",
    "IDEL2",
    "IDEE1",
    "IDEE2",
    "IDGND",
    "IDME",
    "INBGS",
    "IMRTB",
    "IGRTS",
    "IANE",
    "ICN",
    "IAN",
    "IZT1",
    "IZ1T2",
    "IZ2T2",
]

直流场电流模拟量_字段名 = [
    "PPR1A",
    "PPR1B",
    "PPR1C",
    "PPR2A",
    "PPR2B",
    "PPR2C"
]


# CPR/CCP/PCP
直流场电压模拟量 = [
    "UDL",
    "UDM",
    "UDN"
]

直流场电压模拟量_字段名 = [
    "CPR11A",
    "CPR11B",
    "CPR11C",
    "CPR12A",
    "CPR12B",
    "CPR12C",
    "CPR21A",
    "CPR21B",
    "CPR21C",
    "CPR22A",
    "CPR22B",
    "CPR22C",
    "PPR1A",
    "PPR1B",
    "PPR1C",
    "PPR2A",
    "PPR2B",
    "PPR2C"
]


直流场电压模拟量_PCP_CCP = [
    "UDL_IN",
    "UDM_IN",
    "UDN_IN",
]

直流场电压模拟量_PCP_CCP_字段名 = [
    "PCP1A",
    "PCP1B",
    "PCP2A",
    "PCP2B",
    "CCP11A",
    "CCP11B",
    "CCP12A",
    "CCP12B",
    "CCP21A",
    "CCP21B",
    "CCP22A",
    "CCP22B",
]

换流变模拟量 = [
    "YY换流变中性点电流",
    "YD换流变中性点电流"
]

换流变模拟量_字段名 = [
    "CPR11A",
    "CPR11B",
    "CPR11C",
    "CPR12A",
    "CPR12B",
    "CPR12C",
    "CPR21A",
    "CPR21B",
    "CPR21C",
    "CPR22A",
    "CPR22B",
    "CPR22C"
]

直流场总模拟量 = [
    {
        "display_name": "Z1.T3(R1)",
        "data_names": ["IZ1R",],
        "Child": "Child4",
        "From": [
            "P1PPRA",
            "P1PPRB",
            "P1PPRC",
            "P2PPRA",
            "P2PPRB",
            "P2PPRC",
        ]
    },
    {
        "display_name": "Z1.T4(L2)",
        "data_names": ["IZ1L2",],
        "Child": "Child4",
        "From": [
            "P1PPRA",
            "P1PPRB",
            "P1PPRC",
            "P2PPRA",
            "P2PPRB",
            "P2PPRC",
        ]
    },
    {
        "display_name": "Z1.T5(F1)",
        "data_names": ["IAZ1",],
        "Child": "Child0",
        "From": [
            "P1PPRA",
            "P1PPRB",
            "P1PPRC",
            "P2PPRA",
            "P2PPRB",
            "P2PPRC",
        ]
    },
    {
        "display_name": "Z2.T3(R1)",
        "data_names": ["IZ2R",],
        "Child": "Child4",
        "From": [
            "P1PPRA",
            "P1PPRB",
            "P1PPRC",
            "P2PPRA",
            "P2PPRB",
            "P2PPRC",
        ]
    },
    {
        "display_name": "Z2.T4(L2)",
        "data_names": ["IZ2L2",],
        "Child": "Child4",
        "From": [
            "P1PPRA",
            "P1PPRB",
            "P1PPRC",
            "P2PPRA",
            "P2PPRB",
            "P2PPRC",
        ]
    },
    {
        "display_name": "Z2.T5(F1)",
        "data_names": ["IAZ2",],
        "Child": "Child0",
        "From": [
            "P1PPRA",
            "P1PPRB",
            "P1PPRC",
            "P2PPRA",
            "P2PPRB",
            "P2PPRC",
        ]
    },
    {
        "display_name": "P1Udl",
        "data_names": ["UDL", "UDL_IN",],
        "Child": "Child0",
        "From": [
            "P1CCP1A",
            "P1CCP1B",
            "P1CPR1A",
            "P1CPR1B",
            "P1CPR1C",
            "P1CCP2A",
            "P1CCP2B",
            "P1CPR2A",
            "P1CPR2B",
            "P1CPR2C",
            "P1PCPA",
            "P1PCPB",
            "P1PPRA",
            "P1PPRB",
            "P1PPRC",
        ]
    },
    {
        "display_name": "P1Udn",
        "data_names": ["UDN", "UDN_IN",],
        "Child": "Child0",
        "From": [
            "P1CCP1A",
            "P1CCP1B",
            "P1CPR1A",
            "P1CPR1B",
            "P1CPR1C",
            "P1CCP2A",
            "P1CCP2B",
            "P1CPR2A",
            "P1CPR2B",
            "P1CPR2C",
            "P1PCPA",
            "P1PCPB",
            "P1PPRA",
            "P1PPRB",
            "P1PPRC",
        ]
    },
    {
        "display_name": "P1Udm",
        "data_names": ["UDM", "UDM_IN",],
        "Child": "Child0",
        "From": [
            "P1CCP1A",
            "P1CCP1B",
            "P1CPR1A",
            "P1CPR1B",
            "P1CPR1C",
            "P1CCP2A",
            "P1CCP2B",
            "P1CPR2A",
            "P1CPR2B",
            "P1CPR2C",
            "P1PCPA",
            "P1PCPB",
        ]
    },
    {
        "display_name": "P2Udl",
        "data_names": ["UDL", "UDL_IN",],
        "Child": "Child0",
        "From": [
            "P2CCP1A",
            "P2CCP1B",
            "P2CPR1A",
            "P2CPR1B",
            "P2CPR1C",
            "P2CCP2A",
            "P2CCP2B",
            "P2CPR2A",
            "P2CPR2B",
            "P2CPR2C",
            "P2PCPA",
            "P2PCPB",
            "P2PPRA",
            "P2PPRB",
            "P2PPRC",
        ]
    },
    {
        "display_name": "P2Udn",
        "data_names": ["UDN", "UDN_IN",],
        "Child": "Child0",
        "From": [
            "P2CCP1A",
            "P2CCP1B",
            "P2CPR1A",
            "P2CPR1B",
            "P2CPR1C",
            "P2CCP2A",
            "P2CCP2B",
            "P2CPR2A",
            "P2CPR2B",
            "P2CPR2C",
            "P2PCPA",
            "P2PCPB",
            "P2PPRA",
            "P2PPRB",
            "P2PPRC",
        ]
    },
    {
        "display_name": "P2Udm",
        "data_names": ["UDM", "UDM_IN",],
        "Child": "Child0",
        "From": [
            "P2CCP1A",
            "P2CCP1B",
            "P2CPR1A",
            "P2CPR1B",
            "P2CPR1C",
            "P2CCP2A",
            "P2CCP2B",
            "P2CPR2A",
            "P2CPR2B",
            "P2CPR2C",
            "P2PCPA",
            "P2PCPB",
        ]
    },
    {
        "display_name": "IDNC1",
        "data_names": ["IDNC", "IDNC_IN",],
        "Child": "Child0",
        "From": [
            "P1CCP1A",
            "P1CCP1B",
            "P1CPR1A",
            "P1CPR1B",
            "P1CPR1C",
            "P1CCP2A",
            "P1CCP2B",
            "P1CPR2A",
            "P1CPR2B",
            "P1CPR2C",
            "P1PCPA",
            "P1PCPB",
            "P1PPRA",
            "P1PPRB",
            "P1PPRC",
        ]
    },
    {
        "display_name": "IDNE1",
        "data_names": ["IDNE", "IDNE_IN",],
        "Child": "Child0",
        "From": [
            "P1CCP1A",
            "P1CCP1B",
            "P1CPR1A",
            "P1CPR1B",
            "P1CPR1C",
            "P1CCP2A",
            "P1CCP2B",
            "P1CPR2A",
            "P1CPR2B",
            "P1CPR2C",
            "P1PCPA",
            "P1PCPB",
            "P1PPRA",
            "P1PPRB",
            "P1PPRC",
        ]
    },
    {
        "display_name": "IDNC2",
        "data_names": ["IDNC", "IDNC_IN",],
        "Child": "Child0",
        "From": [
            "P2CCP1A",
            "P2CCP1B",
            "P2CPR1A",
            "P2CPR1B",
            "P2CPR1C",
            "P2CCP2A",
            "P2CCP2B",
            "P2CPR2A",
            "P2CPR2B",
            "P2CPR2C",
            "P2PCPA",
            "P2PCPB",
            "P2PPRA",
            "P2PPRB",
            "P2PPRC",
        ]
    },
    {
        "display_name": "IDNE2",
        "data_names": ["IDNE", "IDNE_IN",],
        "Child": "Child0",
        "From": [
            "P2CCP1A",
            "P2CCP1B",
            "P2CPR1A",
            "P2CPR1B",
            "P2CPR1C",
            "P2CCP2A",
            "P2CCP2B",
            "P2CPR2A",
            "P2CPR2B",
            "P2CPR2C",
            "P2PCPA",
            "P2PCPB",
            "P2PPRA",
            "P2PPRB",
            "P2PPRC",
        ]
    },
    {
        "display_name": "IDME",
        "data_names": ["IDNE",],
        "Child": "Child0",
        "From": [
            "P1PCPA",
            "P1PCPB",
            "P1PPRA",
            "P1PPRB",
            "P1PPRC",
            "P2PCPA",
            "P2PCPB",
            "P2PPRA",
            "P2PPRB",
            "P2PPRC",
        ]
    },
    {
        "display_name": "IDGND_M",
        "data_names": ["IDGND_M",],
        "Child": "Child0",
        "From": [
            "P1PCPA",
            "P1PCPB",
            "P1PPRA",
            "P1PPRB",
            "P1PPRC",
            "P2PCPA",
            "P2PCPB",
            "P2PPRA",
            "P2PPRB",
            "P2PPRC",
        ]
    },
    {
        "display_name": "IDGND_P",
        "data_names": ["IDGND",],
        "Child": "Child0",
        "From": [
            "P1PCPA",
            "P1PCPB",
            "P1PPRA",
            "P1PPRB",
            "P1PPRC",
            "P2PCPA",
            "P2PCPB",
            "P2PPRA",
            "P2PPRB",
            "P2PPRC",
        ]
    },
    {
        "display_name": "IDEL1_M",
        "data_names": ["IDEL1_M",],
        "Child": "Child0",
        "From": [
            "P1PCPA",
            "P1PCPB",
            "P1PPRA",
            "P1PPRB",
            "P1PPRC",
            "P2PCPA",
            "P2PCPB",
            "P2PPRA",
            "P2PPRB",
            "P2PPRC",
        ]
    },
    {
        "display_name": "IDEL1_P",
        "data_names": ["IDEL1", "IDEL",],
        "Child": "Child0",
        "From": [
            "P1PCPA",
            "P1PCPB",
            "P1PPRA",
            "P1PPRB",
            "P1PPRC",
            "P2PCPA",
            "P2PCPB",
            "P2PPRA",
            "P2PPRB",
            "P2PPRC",
        ]
    },
    {
        "display_name": "IDEL2_M",
        "data_names": ["IDEL2_M",],
        "Child": "Child0",
        "From": [
            "P1PCPA",
            "P1PCPB",
            "P1PPRA",
            "P1PPRB",
            "P1PPRC",
            "P2PCPA",
            "P2PCPB",
            "P2PPRA",
            "P2PPRB",
            "P2PPRC",
        ]
    },
    {
        "display_name": "IDEL2_P",
        "data_names": ["IDEL2",],
        "Child": "Child0",
        "From": [
            "P1PCPA",
            "P1PCPB",
            "P1PPRA",
            "P1PPRB",
            "P1PPRC",
            "P2PCPA",
            "P2PCPB",
            "P2PPRA",
            "P2PPRB",
            "P2PPRC",
        ]
    },
    {
        "display_name": "P1IDL",
        "data_names": ["IDL",],
        "Child": "Child0",
        "From": [
            "P1PCPA",
            "P1PCPB",
            "P1PPRA",
            "P1PPRB",
            "P1PPRC",
        ]
    },
    {
        "display_name": "P1IDC1P",
        "data_names": ["IDC1P",],
        "Child": "Child0",
        "From": [
            "P1CPR1A",
            "P1CPR1B",
            "P1CPR1C",
            "P1CPR2A",
            "P1CPR2B",
            "P1CPR2C",
            "P1PCPA",
            "P1PCPB",
            "P1PPRA",
            "P1PPRB",
            "P1PPRC",

        ]
    },
    {
        "display_name": "P1IDC1N",
        "data_names": ["IDC1N",],
        "Child": "Child0",
        "From": [
            "P1CPR1A",
            "P1CPR1B",
            "P1CPR1C",
            "P1CPR2A",
            "P1CPR2B",
            "P1CPR2C",
            "P1PCPA",
            "P1PCPB",
            "P1PPRA",
            "P1PPRB",
            "P1PPRC",

        ]
    },
    {
        "display_name": "P1IDC2P",
        "data_names": ["IDC2P",],
        "Child": "Child0",
        "From": [
            "P1CPR1A",
            "P1CPR1B",
            "P1CPR1C",
            "P1CPR2A",
            "P1CPR2B",
            "P1CPR2C",
            "P1PCPA",
            "P1PCPB",
            "P1PPRA",
            "P1PPRB",
            "P1PPRC",

        ]
    },
    {
        "display_name": "P1IDC2N",
        "data_names": ["IDC2N",],
        "Child": "Child0",
        "From": [
            "P1CPR1A",
            "P1CPR1B",
            "P1CPR1C",
            "P1CPR2A",
            "P1CPR2B",
            "P1CPR2C",
            "P1PCPA",
            "P1PCPB",
            "P1PPRA",
            "P1PPRB",
            "P1PPRC",

        ]
    },
    {
        "display_name": "P1ICN",
        "data_names": ["ICN",],
        "Child": "Child0",
        "From": [
            "P1PPRA",
            "P1PPRB",
            "P1PPRC",
        ]
    },
    {
        "display_name": "P1IAN",
        "data_names": ["IAN",],
        "Child": "Child0",
        "From": [
            "P1PPRA",
            "P1PPRB",
            "P1PPRC",
        ]
    },
    {
        "display_name": "P1IZT1",
        "data_names": ["IZT1",],
        "Child": "Child0",
        "From": [
            "P1PPRA",
            "P1PPRB",
            "P1PPRC",
        ]
    },
    {
        "display_name": "P1IZ1T11",
        "data_names": ["IUNB_Z1T11",],
        "Child": "Child4",
        "From": [
            "P1PPRA",
            "P1PPRB",
            "P1PPRC",
        ]
    },
    {
        "display_name": "P1IZ1T12",
        "data_names": ["IUNB_Z1T12",],
        "Child": "Child4",
        "From": [
            "P1PPRA",
            "P1PPRB",
            "P1PPRC",
        ]
    },
    {
        "display_name": "P1IZ1T2",
        "data_names": ["IZ1T2",],
        "Child": "Child0",
        "From": [
            "P1PPRA",
            "P1PPRB",
            "P1PPRC",
        ]
    },
    {
        "display_name": "P1IZ2T1",
        "data_names": ["IUNB_ZZ1T2",],
        "Child": "Child4",
        "From": [
            "P1PPRA",
            "P1PPRB",
            "P1PPRC",
        ]
    },
    {
        "display_name": "P1IZ2T2",
        "data_names": ["IZ2T2",],
        "Child": "Child0",
        "From": [
            "P1PPRA",
            "P1PPRB",
            "P1PPRC",
        ]
    },


    {
        "display_name": "P2IDL",
        "data_names": ["IDL",],
        "Child": "Child0",
        "From": [
            "P2PCPA",
            "P2PCPB",
            "P2PPRA",
            "P2PPRB",
            "P2PPRC",
        ]
    },
    {
        "display_name": "P2IDC1P",
        "data_names": ["IDC1P",],
        "Child": "Child0",
        "From": [
            "P2CPR1A",
            "P2CPR1B",
            "P2CPR1C",
            "P2CPR2A",
            "P2CPR2B",
            "P2CPR2C",
            "P2PCPA",
            "P2PCPB",
            "P2PPRA",
            "P2PPRB",
            "P2PPRC",

        ]
    },
    {
        "display_name": "P2IDC1N",
        "data_names": ["IDC1N",],
        "Child": "Child0",
        "From": [
            "P2CPR1A",
            "P2CPR1B",
            "P2CPR1C",
            "P2CPR2A",
            "P2CPR2B",
            "P2CPR2C",
            "P2PCPA",
            "P2PCPB",
            "P2PPRA",
            "P2PPRB",
            "P2PPRC",

        ]
    },
    {
        "display_name": "P2IDC2P",
        "data_names": ["IDC2P",],
        "Child": "Child0",
        "From": [
            "P2CPR1A",
            "P2CPR1B",
            "P2CPR1C",
            "P2CPR2A",
            "P2CPR2B",
            "P2CPR2C",
            "P2PCPA",
            "P2PCPB",
            "P2PPRA",
            "P2PPRB",
            "P2PPRC",

        ]
    },
    {
        "display_name": "P2IDC2N",
        "data_names": ["IDC2N",],
        "Child": "Child0",
        "From": [
            "P2CPR1A",
            "P2CPR1B",
            "P2CPR1C",
            "P2CPR2A",
            "P2CPR2B",
            "P2CPR2C",
            "P2PCPA",
            "P2PCPB",
            "P2PPRA",
            "P2PPRB",
            "P2PPRC",

        ]
    },
    {
        "display_name": "P2ICN",
        "data_names": ["ICN",],
        "Child": "Child0",
        "From": [
            "P2PPRA",
            "P2PPRB",
            "P2PPRC",
        ]
    },
    {
        "display_name": "P2IAN",
        "data_names": ["IAN",],
        "Child": "Child0",
        "From": [
            "P2PPRA",
            "P2PPRB",
            "P2PPRC",
        ]
    },
    {
        "display_name": "P2IZT1",
        "data_names": ["IZT1",],
        "Child": "Child0",
        "From": [
            "P2PPRA",
            "P2PPRB",
            "P2PPRC",
        ]
    },
    {
        "display_name": "P2IZ1T11",
        "data_names": ["IUNB_Z1T11",],
        "Child": "Child4",
        "From": [
            "P2PPRA",
            "P2PPRB",
            "P2PPRC",
        ]
    },
    {
        "display_name": "P2IZ1T12",
        "data_names": ["IUNB_Z1T12",],
        "Child": "Child4",
        "From": [
            "P2PPRA",
            "P2PPRB",
            "P2PPRC",
        ]
    },
    {
        "display_name": "P2IZ1T2",
        "data_names": ["IZ1T2",],
        "Child": "Child0",
        "From": [
            "P2PPRA",
            "P2PPRB",
            "P2PPRC",
        ]
    },
    {
        "display_name": "P2IZ2T1",
        "data_names": ["IUNB_ZZ1T2",],
        "Child": "Child4",
        "From": [
            "P2PPRA",
            "P2PPRB",
            "P2PPRC",
        ]
    },
    {
        "display_name": "P2IZ2T2",
        "data_names": ["IZ2T2",],
        "Child": "Child0",
        "From": [
            "P2PPRA",
            "P2PPRB",
            "P2PPRC",
        ]
    },
    {
        "display_name": "P1INBS",
        "data_names": ["INBS",],
        "Child": "Child0",
        "From": [
            "P1PPRA",
            "P1PPRB",
            "P1PPRC",
        ]
    },
    {
        "display_name": "P2INBS",
        "data_names": ["INBS",],
        "Child": "Child0",
        "From": [
            "P2PPRA",
            "P2PPRB",
            "P2PPRC",
        ]
    },
    {
        "display_name": "INBGS",
        "data_names": ["INBGS",],
        "Child": "Child0",
        "From": [
            "P1PPRA",
            "P1PPRB",
            "P1PPRC",
            "P2PPRA",
            "P2PPRB",
            "P2PPRC",
        ]
    },
    {
        "display_name": "IDEE1",
        "data_names": ["IDEE1",],
        "Child": "Child0",
        "From": [
            "P1PPRA",
            "P1PPRB",
            "P1PPRC",
            "P2PPRA",
            "P2PPRB",
            "P2PPRC",
        ]
    },
    {
        "display_name": "IDEE2",
        "data_names": ["IDEE2",],
        "Child": "Child0",
        "From": [
            "P1PPRA",
            "P1PPRB",
            "P1PPRC",
            "P2PPRA",
            "P2PPRB",
            "P2PPRC",
        ]
    },
]

带极总字段 = [
    "P1CCP1A",
    "P1CCP1B",
    "P1CPR1A",
    "P1CPR1B",
    "P1CPR1C",
    "P1CCP2A",
    "P1CCP2B",
    "P1CPR2A",
    "P1CPR2B",
    "P1CPR2C",
    "P1PCPA",
    "P1PCPB",
    "P1PPRA",
    "P1PPRB",
    "P1PPRC",
    "P2CCP1A",
    "P2CCP1B",
    "P2CPR1A",
    "P2CPR1B",
    "P2CPR1C",
    "P2CCP2A",
    "P2CCP2B",
    "P2CPR2A",
    "P2CPR2B",
    "P2CPR2C",
    "P2PCPA",
    "P2PCPB",
    "P2PPRA",
    "P2PPRB",
    "P2PPRC",
]

