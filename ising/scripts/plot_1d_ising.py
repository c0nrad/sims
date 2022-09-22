import matplotlib.pyplot as plot
import numpy as np
import math

forced_Ts = np.linspace(5, 0.1, 50)

forced_symmetry_results = {
    'uuu': [
        0.1986,
        0.19450000000000006,
        0.20124000000000003,
        0.20308000000000004,
        0.20313999999999993,
        0.20472000000000004,
        0.20604000000000006,
        0.21144,
        0.2091200000000002,
        0.21024,
        0.21386000000000013,
        0.21609999999999988,
        0.21774000000000007,
        0.22024000000000007,
        0.21728000000000006,
        0.22155999999999995,
        0.23088000000000009,
        0.2304200000000001,
        0.23343999999999998,
        0.2437,
        0.24431999999999998,
        0.24492,
        0.2488399999999999,
        0.25379999999999997,
        0.26020000000000015,
        0.26014,
        0.27034,
        0.2806000000000001,
        0.28007999999999994,
        0.28879999999999995,
        0.29460000000000003,
        0.30324,
        0.3152400000000001,
        0.3219199999999999,
        0.33793999999999996,
        0.3454399999999998,
        0.3598000000000001,
        0.37088,
        0.39802000000000015,
        0.41391999999999984,
        0.4343600000000001,
        0.4581599999999999,
        0.48972000000000016,
        0.51836,
        0.5595600000000001,
        0.6031800000000003,
        0.7255600000000002,
        0.8813,
        1.0,
        1.0,
    ],
    'uud': [
        0.12261999999999997,
        0.12373999999999999,
        0.12113999999999996,
        0.12155999999999997,
        0.12148000000000007,
        0.12210000000000004,
        0.12094000000000006,
        0.11954,
        0.12154,
        0.12129999999999998,
        0.11992000000000003,
        0.11858000000000006,
        0.11897999999999997,
        0.11944000000000005,
        0.11901999999999999,
        0.11869999999999997,
        0.11629999999999997,
        0.11695999999999993,
        0.11452,
        0.11552000000000005,
        0.11391999999999998,
        0.11367999999999996,
        0.11227999999999999,
        0.11092000000000002,
        0.10994000000000001,
        0.10958,
        0.10667999999999994,
        0.10554000000000004,
        0.10421999999999997,
        0.10244,
        0.09988,
        0.09876000000000003,
        0.09425999999999998,
        0.09101999999999999,
        0.08815999999999997,
        0.08351999999999996,
        0.07917999999999999,
        0.07471999999999998,
        0.06783999999999994,
        0.06145999999999998,
        0.05201999999999998,
        0.043879999999999975,
        0.035159999999999976,
        0.025380000000000003,
        0.016280000000000013,
        0.009280000000000007,
        0.003320000000000002,
        0.0008200000000000006,
        0.0,
        0.0,
    ],
    'udu': [
        0.08365999999999996,
        0.08242,
        0.08127999999999994,
        0.0795,
        0.08237999999999995,
        0.07905999999999999,
        0.07759999999999997,
        0.07632,
        0.07565999999999998,
        0.07538000000000002,
        0.07479999999999999,
        0.07147999999999999,
        0.07123999999999998,
        0.07083999999999999,
        0.06971999999999998,
        0.06813999999999999,
        0.06555999999999998,
        0.06445999999999998,
        0.06215999999999997,
        0.06019999999999997,
        0.05864,
        0.057219999999999965,
        0.05601999999999998,
        0.05389999999999999,
        0.05099999999999997,
        0.051519999999999955,
        0.0463,
        0.044959999999999986,
        0.04319999999999999,
        0.04213999999999995,
        0.03881999999999995,
        0.03547999999999998,
        0.032259999999999976,
        0.028859999999999986,
        0.027319999999999994,
        0.022540000000000004,
        0.018340000000000013,
        0.016860000000000014,
        0.01384000000000001,
        0.010920000000000008,
        0.006840000000000005,
        0.004680000000000003,
        0.002900000000000002,
        0.0016400000000000008,
        0.0007400000000000005,
        0.00022000000000000006,
        4e-05,
        0.0,
        0.0,
        0.0,
    ],
    'udd': [
        0.11642,
        0.11878000000000002,
        0.11673999999999994,
        0.11774000000000001,
        0.11584,
        0.11575999999999995,
        0.11735999999999999,
        0.11630000000000003,
        0.11586000000000002,
        0.11602000000000003,
        0.11513999999999999,
        0.11520000000000001,
        0.11498,
        0.11474000000000005,
        0.11405999999999997,
        0.11424,
        0.11166000000000002,
        0.11250000000000002,
        0.11194000000000008,
        0.10917999999999997,
        0.10972000000000003,
        0.10865999999999999,
        0.10882,
        0.10820000000000003,
        0.10545999999999997,
        0.106,
        0.10324000000000001,
        0.10122000000000003,
        0.1007,
        0.09850000000000002,
        0.09621999999999993,
        0.09381999999999997,
        0.09223999999999996,
        0.08843999999999994,
        0.08468,
        0.0816,
        0.07833999999999994,
        0.07256,
        0.06547999999999997,
        0.05945999999999995,
        0.052119999999999965,
        0.043499999999999976,
        0.03485999999999998,
        0.02515999999999999,
        0.016060000000000012,
        0.009160000000000007,
        0.0032800000000000025,
        0.0008200000000000006,
        0.0,
        0.0,
    ],
    'duu': [
        0.12261999999999997,
        0.12373999999999999,
        0.12113999999999996,
        0.12155999999999997,
        0.12148000000000007,
        0.12210000000000004,
        0.12094000000000006,
        0.11954,
        0.12154,
        0.12129999999999998,
        0.11992000000000003,
        0.11858000000000006,
        0.11897999999999997,
        0.11944000000000005,
        0.11901999999999999,
        0.11869999999999997,
        0.11629999999999997,
        0.11695999999999993,
        0.11452,
        0.11552000000000005,
        0.11391999999999998,
        0.11367999999999996,
        0.11227999999999999,
        0.11092000000000002,
        0.10994000000000001,
        0.10958,
        0.10667999999999994,
        0.10554000000000004,
        0.10421999999999997,
        0.10244,
        0.09988,
        0.09876000000000003,
        0.09425999999999998,
        0.09101999999999999,
        0.08815999999999997,
        0.08351999999999996,
        0.07917999999999999,
        0.07471999999999998,
        0.06783999999999994,
        0.06145999999999998,
        0.05201999999999998,
        0.043879999999999975,
        0.035159999999999976,
        0.025380000000000003,
        0.016280000000000013,
        0.009280000000000007,
        0.003320000000000002,
        0.0008200000000000006,
        0.0,
        0.0,
    ],
    'dud': [
        0.07745999999999999,
        0.07745999999999999,
        0.07687999999999999,
        0.07567999999999997,
        0.07673999999999997,
        0.07271999999999998,
        0.07401999999999999,
        0.07308000000000002,
        0.06997999999999996,
        0.07010000000000001,
        0.07001999999999999,
        0.06810000000000001,
        0.06723999999999997,
        0.06613999999999998,
        0.06475999999999997,
        0.06368,
        0.06092000000000002,
        0.059999999999999935,
        0.05957999999999999,
        0.05385999999999998,
        0.05443999999999996,
        0.05219999999999996,
        0.05255999999999996,
        0.05117999999999997,
        0.046519999999999964,
        0.047939999999999976,
        0.04285999999999998,
        0.040639999999999954,
        0.03967999999999997,
        0.038199999999999984,
        0.03515999999999998,
        0.03053999999999999,
        0.030239999999999986,
        0.02627999999999999,
        0.023839999999999993,
        0.020620000000000013,
        0.017500000000000012,
        0.014700000000000012,
        0.011480000000000008,
        0.008920000000000006,
        0.006940000000000005,
        0.0043000000000000035,
        0.0026000000000000016,
        0.0014200000000000007,
        0.0005200000000000002,
        0.0001,
        0.0,
        0.0,
        0.0,
        0.0,
    ],
    'ddu': [
        0.11642,
        0.11878000000000002,
        0.11673999999999994,
        0.11774000000000001,
        0.11584,
        0.11575999999999995,
        0.11735999999999999,
        0.11630000000000003,
        0.11586000000000002,
        0.11602000000000003,
        0.11513999999999999,
        0.11520000000000001,
        0.11498,
        0.11474000000000005,
        0.11405999999999997,
        0.11424,
        0.11166000000000002,
        0.11250000000000002,
        0.11194000000000008,
        0.10917999999999997,
        0.10972000000000003,
        0.10865999999999999,
        0.10882,
        0.10820000000000003,
        0.10545999999999997,
        0.106,
        0.10324000000000001,
        0.10122000000000003,
        0.1007,
        0.09850000000000002,
        0.09621999999999993,
        0.09381999999999997,
        0.09223999999999996,
        0.08843999999999994,
        0.08468,
        0.0816,
        0.07833999999999994,
        0.07256,
        0.06547999999999997,
        0.05945999999999995,
        0.052119999999999965,
        0.043499999999999976,
        0.03485999999999998,
        0.02515999999999999,
        0.016060000000000012,
        0.009160000000000007,
        0.0032800000000000025,
        0.0008200000000000006,
        0.0,
        0.0,
    ],
    'ddd': [
        0.1622000000000001,
        0.16058000000000003,
        0.16484000000000004,
        0.16314,
        0.16310000000000005,
        0.16778,
        0.16574000000000005,
        0.16748000000000002,
        0.17044000000000004,
        0.16964,
        0.1711999999999999,
        0.17675999999999997,
        0.17586,
        0.17442000000000005,
        0.18208000000000002,
        0.18074000000000012,
        0.18672000000000008,
        0.18620000000000003,
        0.19190000000000002,
        0.19284000000000007,
        0.19531999999999997,
        0.20097999999999996,
        0.20038000000000017,
        0.20288000000000006,
        0.21148,
        0.20924000000000004,
        0.22066000000000002,
        0.22028000000000003,
        0.22720000000000007,
        0.22898000000000004,
        0.23922000000000004,
        0.24558,
        0.24926,
        0.26402000000000003,
        0.26522000000000007,
        0.2811599999999999,
        0.28931999999999997,
        0.30299999999999994,
        0.31002,
        0.32439999999999997,
        0.34358000000000005,
        0.3581,
        0.3647399999999999,
        0.37750000000000006,
        0.37450000000000017,
        0.35962000000000005,
        0.2612,
        0.11542000000000002,
        0.0,
        0.0,
    ],
}
Ts = np.linspace(5, 0.1, 50)


results = {
    'uuu': [
        0.17892000000000002,
        0.18189999999999998,
        0.18180999999999997,
        0.18450999999999992,
        0.18112999999999999,
        0.18540000000000004,
        0.18660000000000004,
        0.19094999999999987,
        0.19137,
        0.19282999999999997,
        0.19579000000000002,
        0.19214000000000006,
        0.19929999999999995,
        0.20250999999999997,
        0.19867999999999988,
        0.2043,
        0.21054000000000006,
        0.20848,
        0.20922999999999997,
        0.21654000000000007,
        0.2195899999999999,
        0.21988,
        0.22237999999999997,
        0.22646000000000016,
        0.2333199999999999,
        0.2376500000000001,
        0.23868000000000003,
        0.24935,
        0.2524700000000001,
        0.26152000000000014,
        0.2691499999999999,
        0.27810000000000007,
        0.28265999999999997,
        0.2874900000000001,
        0.3026599999999999,
        0.30605,
        0.33033999999999997,
        0.34491999999999995,
        0.35928000000000004,
        0.3675399999999999,
        0.38765999999999984,
        0.4061499999999999,
        0.42971,
        0.4375499999999999,
        0.46186999999999984,
        0.48345000000000005,
        0.45935999999999977,
        0.7329099999999998,
        1.0,
        1.0,
    ],
    'uud': [
        0.11981,
        0.12042000000000001,
        0.11927000000000001,
        0.12009000000000002,
        0.11877000000000003,
        0.11861000000000002,
        0.11871999999999998,
        0.11858999999999999,
        0.11655000000000004,
        0.11814000000000002,
        0.11771000000000001,
        0.11742,
        0.11528,
        0.11642000000000001,
        0.11726000000000009,
        0.11598000000000006,
        0.11556000000000007,
        0.11460999999999999,
        0.11322000000000004,
        0.11356000000000004,
        0.11264000000000003,
        0.11190000000000005,
        0.11006000000000007,
        0.10925000000000008,
        0.10785000000000004,
        0.10716000000000003,
        0.10565000000000001,
        0.10344000000000005,
        0.10184000000000004,
        0.10040000000000004,
        0.09838000000000002,
        0.09638,
        0.09242000000000004,
        0.09032000000000004,
        0.08662000000000003,
        0.08291,
        0.07762999999999998,
        0.07285,
        0.06610000000000003,
        0.06049999999999998,
        0.052620000000000014,
        0.04418999999999998,
        0.03522,
        0.024999999999999988,
        0.016729999999999988,
        0.008750000000000006,
        0.0032500000000000025,
        0.0011200000000000008,
        0.0,
        0.0,
    ],
    'udu': [
        0.07965,
        0.08133000000000001,
        0.07878000000000002,
        0.07889000000000002,
        0.07802000000000002,
        0.07639000000000001,
        0.07631000000000002,
        0.07402,
        0.07126000000000002,
        0.07258999999999997,
        0.07363000000000001,
        0.07005,
        0.06941999999999998,
        0.06895000000000003,
        0.06594000000000001,
        0.06451999999999997,
        0.06352000000000003,
        0.061610000000000026,
        0.06112,
        0.060020000000000004,
        0.05782999999999996,
        0.05579999999999998,
        0.05322000000000001,
        0.05243000000000002,
        0.04999,
        0.04854999999999997,
        0.04512999999999999,
        0.043789999999999975,
        0.04185,
        0.037549999999999986,
        0.036209999999999985,
        0.03361999999999999,
        0.030019999999999998,
        0.02831999999999999,
        0.025119999999999983,
        0.02134999999999999,
        0.01863999999999999,
        0.01629999999999999,
        0.012469999999999997,
        0.009400000000000007,
        0.006670000000000005,
        0.004900000000000004,
        0.002800000000000002,
        0.001340000000000001,
        0.0006300000000000002,
        0.00010000000000000002,
        4e-05,
        1e-05,
        0.0,
        0.0,
    ],
    'udd': [
        0.12131000000000004,
        0.11815000000000003,
        0.11908000000000003,
        0.11812000000000004,
        0.1195000000000001,
        0.11869000000000003,
        0.11932000000000001,
        0.11808000000000002,
        0.11897000000000008,
        0.1178400000000001,
        0.11690000000000006,
        0.11795,
        0.11526000000000002,
        0.11531000000000004,
        0.11706000000000001,
        0.11592000000000006,
        0.11538,
        0.11488000000000004,
        0.11415000000000004,
        0.11313000000000008,
        0.11220000000000002,
        0.11178000000000005,
        0.11101000000000003,
        0.10958000000000004,
        0.10766000000000002,
        0.10690000000000012,
        0.10708000000000004,
        0.10384000000000004,
        0.10197,
        0.10049999999999999,
        0.09835000000000005,
        0.09535000000000003,
        0.09363000000000002,
        0.09064000000000005,
        0.08630999999999998,
        0.08348000000000005,
        0.07758000000000001,
        0.07234999999999998,
        0.06584000000000004,
        0.060349999999999994,
        0.052729999999999985,
        0.04437999999999999,
        0.035279999999999985,
        0.02518999999999998,
        0.016729999999999988,
        0.008870000000000006,
        0.0032300000000000024,
        0.0011100000000000007,
        0.0,
        0.0,
    ],
    'duu': [
        0.11981,
        0.12042000000000001,
        0.11927000000000001,
        0.12009000000000002,
        0.11877000000000003,
        0.11861000000000002,
        0.11871999999999998,
        0.11858999999999999,
        0.11655000000000004,
        0.11814000000000002,
        0.11771000000000001,
        0.11742,
        0.11528,
        0.11642000000000001,
        0.11726000000000009,
        0.11598000000000006,
        0.11556000000000007,
        0.11460999999999999,
        0.11322000000000004,
        0.11356000000000004,
        0.11264000000000003,
        0.11190000000000005,
        0.11006000000000007,
        0.10925000000000008,
        0.10785000000000004,
        0.10716000000000003,
        0.10565000000000001,
        0.10344000000000005,
        0.10184000000000004,
        0.10040000000000004,
        0.09838000000000002,
        0.09638,
        0.09242000000000004,
        0.09032000000000004,
        0.08662000000000003,
        0.08291,
        0.07762999999999998,
        0.07285,
        0.06610000000000003,
        0.06049999999999998,
        0.052620000000000014,
        0.04418999999999998,
        0.03522,
        0.024999999999999988,
        0.016729999999999988,
        0.008750000000000006,
        0.0032500000000000025,
        0.0011200000000000008,
        0.0,
        0.0,
    ],
    'dud': [
        0.08115000000000004,
        0.07906000000000003,
        0.07859,
        0.07691999999999999,
        0.07875000000000001,
        0.07646999999999998,
        0.07691,
        0.07351,
        0.07368000000000001,
        0.07229,
        0.07282000000000002,
        0.07058,
        0.06940000000000002,
        0.06783999999999998,
        0.06573999999999998,
        0.06446,
        0.06334000000000001,
        0.06188,
        0.06205000000000001,
        0.059590000000000004,
        0.05739,
        0.05568000000000002,
        0.05416999999999998,
        0.05276,
        0.04979999999999998,
        0.04828999999999998,
        0.04656,
        0.04418999999999998,
        0.041979999999999976,
        0.03764999999999997,
        0.03617999999999998,
        0.03258999999999999,
        0.03122999999999997,
        0.028639999999999978,
        0.02480999999999998,
        0.02191999999999999,
        0.018589999999999992,
        0.01579999999999999,
        0.012209999999999999,
        0.009250000000000006,
        0.006780000000000005,
        0.005090000000000003,
        0.002860000000000002,
        0.001530000000000001,
        0.0006300000000000005,
        0.00022000000000000012,
        2e-05,
        0.0,
        0.0,
        0.0,
    ],
    'ddu': [
        0.12131000000000004,
        0.11815000000000003,
        0.11908000000000003,
        0.11812000000000004,
        0.1195000000000001,
        0.11869000000000003,
        0.11932000000000001,
        0.11808000000000002,
        0.11897000000000008,
        0.1178400000000001,
        0.11690000000000006,
        0.11795,
        0.11526000000000002,
        0.11531000000000004,
        0.11706000000000001,
        0.11592000000000006,
        0.11538,
        0.11488000000000004,
        0.11415000000000004,
        0.11313000000000008,
        0.11220000000000002,
        0.11178000000000005,
        0.11101000000000003,
        0.10958000000000004,
        0.10766000000000002,
        0.10690000000000012,
        0.10708000000000004,
        0.10384000000000004,
        0.10197,
        0.10049999999999999,
        0.09835000000000005,
        0.09535000000000003,
        0.09363000000000002,
        0.09064000000000005,
        0.08630999999999998,
        0.08348000000000005,
        0.07758000000000001,
        0.07234999999999998,
        0.06584000000000004,
        0.060349999999999994,
        0.052729999999999985,
        0.04437999999999999,
        0.035279999999999985,
        0.02518999999999998,
        0.016729999999999988,
        0.008870000000000006,
        0.0032300000000000024,
        0.0011100000000000007,
        0.0,
        0.0,
    ],
    'ddd': [
        0.17804000000000006,
        0.18056999999999998,
        0.18411999999999998,
        0.18326,
        0.18555999999999995,
        0.18713999999999992,
        0.1841,
        0.1881799999999999,
        0.19264999999999996,
        0.19033000000000005,
        0.1885400000000001,
        0.19648999999999997,
        0.20079999999999998,
        0.19724000000000003,
        0.2009999999999999,
        0.20292000000000002,
        0.20072000000000004,
        0.20905000000000007,
        0.21285999999999997,
        0.21046999999999993,
        0.21551000000000006,
        0.22128,
        0.22809000000000004,
        0.23069000000000006,
        0.23586999999999997,
        0.2373900000000001,
        0.24416999999999997,
        0.24811000000000008,
        0.2560799999999999,
        0.26148000000000005,
        0.26499999999999996,
        0.2722300000000001,
        0.28398999999999996,
        0.29363000000000006,
        0.3015499999999998,
        0.3178999999999999,
        0.32201,
        0.33258000000000004,
        0.35216000000000003,
        0.37211,
        0.38819000000000004,
        0.40672,
        0.42363000000000006,
        0.45919999999999994,
        0.46995,
        0.48098999999999975,
        0.52762,
        0.2626199999999999,
        0.0,
        0.0,
    ],
}

results = forced_symmetry_results

results["duu"] = [sum(value) for value in zip(results["ddu"], results["uud"])]
results["ddu"] = [sum(value) for value in zip(results["ddu"], results["udd"])]
del results["uud"]
del results["udd"]


def e_guess(t):
    print(t)
    out = (1 / 4) * (1 - math.tanh(1 / t) ** 2)
    # out = (1 / 4) * (1 - math.tanh(1 / Ts) ** 2)
    # print(out)
    return out


def f_guess(t):
    # return (1 + math.tanh(1 / t) ** 2) / (4 + 4 * math.exp(4 / t))
    return (1 / 2) / (1 + math.exp(2 / t)) ** 2


def d_guess(t):
    return (1 / 8) * (1 + math.tanh(1 / t)) ** 2
    # 1 / 8(1 + Tanh[1 / t]) ^ 2


def a_guess(t):
    return (1 / 4) * (1 + math.tanh(1 / (4 * t))) ** 2
    # 2/32 (1 + Tanh[1/t])^4, {t, 0, 5}


v = [e_guess(t) for t in Ts]
print(v)
print(Ts)

# for state in results:
# if state[0] == "u":

plot.plot(Ts, results["uuu"], label="uuu")
plot.plot(Ts, results["duu"], label="duu")
plot.plot(Ts, results["dud"], label="dud")
plot.plot(Ts, results["ddd"], label="ddd")
plot.plot(Ts, results["ddu"], label="ddu")
plot.plot(Ts, results["udu"], label="udu")
plot.plot(Ts, [e_guess(t) for t in Ts], label="ddu guess")
plot.plot(Ts, [f_guess(t) for t in Ts], label="udu guess")
plot.plot(Ts, [d_guess(t) for t in Ts], label="ddd guess")
plot.plot(Ts, [a_guess(t) for t in Ts], label="ddd guess")


plot.xlabel("Temperature")
plot.ylabel("Probability")
plot.title("1D Ising State Expectation Values with Fits for ddd, ddu, dud")
plot.legend(loc="upper right")

plot.show()
