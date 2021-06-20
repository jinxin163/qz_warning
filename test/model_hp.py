# -*- coding: utf-8 -*-
# 参考地址云讲座PPT 已确定
# --------------------------------------------
GNSS_HP_01 = {
    "red": {
        "XY_24h": 50,
        "Z_24h": 50,
        "XYZ_24h": 50,
    },
    "orange": {
        "XY_24h": 40,
        "Z_24h": 40,
        "XYZ_24h": 40,
    },
    "yellow": {
        "XY_24h": 30,
        "Z_24h": 30,
        "XYZ_24h": 30,
    },
    "blue": {
        "XY_24h": 20,
        "Z_24h": 20,
        "XYZ_24h": 20,
    }
}

GNSS_HP_01_meaning = {
    "XY_24h": "前24小时水平位移变形速率",
    "Z_24h": "前24小时垂直位移变形速率",
    "XYZ_24h": "前24小时三维位移变形速率",
    "unit": "mm/日"
}

print("GNSS_HP_01")
print(GNSS_HP_01)
print(GNSS_HP_01_meaning)

GNSS_HP_02 = {
    "red": {
        "XY_3d": 80,
        "Z_3d": 80,
        "XYZ_3d": 80,
    },
    "orange": {
        "XY_3d": 60,
        "Z_3d": 60,
        "XYZ_3d": 60,
    },
    "yellow": {
        "XY_3d": 45,
        "Z_3d": 45,
        "XYZ_3d": 45,
    },
    "blue": {
        "XY_3d": 30,
        "Z_3d": 30,
        "XYZ_3d": 30,
    }
}

GNSS_HP_02_meaning = {
    "XY_3d": "前3日水平位移变形量",
    "Z_3d": "前3日垂直位移变形量",
    "XYZ_3d": "前3日三维位移变形量",
    "unit": "mm"
}

print("GNSS_HP_02")
print(GNSS_HP_02)
print(GNSS_HP_02_meaning)

# 参考重庆忠县滑坡模型1 已确定
BMQX_HP_01 = {
    "red": {
        "BMQX01_24h": 20,
        "BMQX02_24h": 20,
        "BMQX03_24h": 20,
    },
    "orange": {
        "BMQX01_24h": 15,
        "BMQX02_24h": 15,
        "BMQX03_24h": 15,
    },
    "yellow": {
        "BMQX01_24h": 10,
        "BMQX02_24h": 10,
        "BMQX03_24h": 10,
    },
    "blue": {
        "BMQX01_24h": 6,
        "BMQX02_24h": 6,
        "BMQX03_24h": 6,
    }
}

BMQX_HP_01_meaning = {
    "BMQX01_24h": "前24小时表面倾斜X轴变化量",
    "BMQX02_24h": "前24小时表面倾斜Y轴变化量",
    "BMQX03_24h": "前24小时表面倾斜Z轴变化量",
    "unit": "度"
}
print("BMQX_HP_01")
print(BMQX_HP_01)
print(BMQX_HP_01_meaning)

# 区布嘎滑坡模型 已确定
DBLF_HP_01 = {
    "red": {
        "DBLF01_24h": 10
    },
    "orange": {
        "DBLF01_24h": 5
    },

    "yellow": {
        "DBLF01_24h": 3
    },
    "blue": {
        "DBLF01_24h": 2
    }
}

DBLF_HP_01_meaning = {
    "DBLF01_24h": "前24小时地表裂缝变形量",
    "unit": "mm"
}
print("DBLF_HP_01")
print(DBLF_HP_01)
print(DBLF_HP_01_meaning)

CJBX = {

}

# 已确定
SBQX_HP_01 = {
    "red": {
        "SBQX01_24h": 20,
        "SBQX02_24h": 20
    },
    "orange": {
        "SBQX01_24h": 15,
        "SBQX02_24h": 15
    },
    "yellow": {
        "SBQX01_24h": 10,
        "SBQX02_24h": 10
    },
    "blue": {
        "SBQX01_24h": 6,
        "SBQX02_24h": 6
    }
}
SBQX_HP_01_meaning = {
    "SBQX01_24h": "前24小时深部倾斜X轴变化量",
    "SBQX02_24h": "前24小时深部倾斜Y轴变化量",
    "unit": "mm"

}
print("SBQX_HP_01")
print(SBQX_HP_01)
print(SBQX_HP_01_meaning)

DBQX = {

}

DXSW = {

}

QXSY = {

}

# 已确定
THSL_HP_01 = {
    "red": {
        "THSL01": 90
    },
    "orange": {
        "THSL01": 80
    },

    "yellow": {
        "THSL01": 70
    },
    "blue": {
        "THSL01": 60
    }
}
THSL_HP_01_meaning = {
    "THSL01": "土含水率实时监测值",
    "unit": "百分数"
}
print("THSL_HP_01")
print(THSL_HP_01)
print(THSL_HP_01_meaning)

MGYL = {

}

TYJC = {

}

# 区布嘎滑坡模型 已确定
JSJC_HP_01 = {
    "red": {
        "JSJC01_1h": 40,
        "JSJC01_12h": 70,
        "JSJC01_24h": 100,
    },
    "orange": {
        "JSJC01_1h": 30,
        "JSJC01_12h": 50,
        "JSJC01_24h": 75,
    },
    "yellow": {
        "JSJC01_1h": 20,
        "JSJC01_12h": 30,
        "JSJC01_24h": 50,
    },
    "blue": {
        "JSJC01_1h": 10,
        "JSJC01_12h": 15,
        "JSJC01_24h": 25,
    }
}
JSJC_HP_01_meaning = {
    "JSJC01_1h": "前1小时的降水量",
    "JSJC01_12h": "前12小时的降水量",
    "JSJC01_24h": "前24小时的降水量",
    "unit": "mm"
}
print("JSJC_HP_01")
print(JSJC_HP_01)
print(JSJC_HP_01_meaning)

QWJC = {

}

ZDJC = {

}
