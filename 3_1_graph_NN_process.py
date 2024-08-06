import re
import matplotlib.pyplot as plt
log_str = """
Epoch: 0001 loss_train: 1.517588 acc_train: 0.483146 loss_val: 0.650657 acc_val: 0.621622 time: 3.954442s
Epoch: 0002 loss_train: 1.349925 acc_train: 0.579775 loss_val: 0.650360 acc_val: 0.621622 time: 9.848730s
Epoch: 0003 loss_train: 1.341258 acc_train: 0.582022 loss_val: 0.655390 acc_val: 0.639640 time: 14.577183s
Epoch: 0004 loss_train: 1.325418 acc_train: 0.624719 loss_val: 0.638073 acc_val: 0.648649 time: 19.395077s
Epoch: 0005 loss_train: 1.310485 acc_train: 0.606742 loss_val: 0.627529 acc_val: 0.648649 time: 23.843339s
Epoch: 0006 loss_train: 1.295386 acc_train: 0.666292 loss_val: 0.631417 acc_val: 0.747748 time: 27.636837s
Epoch: 0007 loss_train: 1.276544 acc_train: 0.678652 loss_val: 0.618912 acc_val: 0.756757 time: 31.840296s
Epoch: 0008 loss_train: 1.265091 acc_train: 0.686517 loss_val: 0.615951 acc_val: 0.765766 time: 36.547528s
Epoch: 0009 loss_train: 1.251761 acc_train: 0.689888 loss_val: 0.620587 acc_val: 0.711712 time: 41.089297s
Epoch: 0010 loss_train: 1.248909 acc_train: 0.674157 loss_val: 0.606223 acc_val: 0.756757 time: 45.010582s
Epoch: 0011 loss_train: 1.237606 acc_train: 0.689888 loss_val: 0.606929 acc_val: 0.738739 time: 49.429636s
Epoch: 0012 loss_train: 1.230120 acc_train: 0.694382 loss_val: 0.602843 acc_val: 0.747748 time: 54.003718s
Epoch: 0013 loss_train: 1.214652 acc_train: 0.701124 loss_val: 0.598286 acc_val: 0.756757 time: 58.176620s
Epoch: 0014 loss_train: 1.213239 acc_train: 0.697753 loss_val: 0.599685 acc_val: 0.729730 time: 62.145802s
Epoch: 0015 loss_train: 1.203889 acc_train: 0.694382 loss_val: 0.589668 acc_val: 0.738739 time: 65.846561s
Epoch: 0016 loss_train: 1.206934 acc_train: 0.697753 loss_val: 0.590160 acc_val: 0.738739 time: 70.669163s
Epoch: 0017 loss_train: 1.193725 acc_train: 0.704494 loss_val: 0.570307 acc_val: 0.756757 time: 74.598148s
Epoch: 0018 loss_train: 1.198875 acc_train: 0.704494 loss_val: 0.580826 acc_val: 0.738739 time: 78.916286s
Epoch: 0019 loss_train: 1.192180 acc_train: 0.700000 loss_val: 0.575538 acc_val: 0.738739 time: 83.071858s
Epoch: 0020 loss_train: 1.181665 acc_train: 0.704494 loss_val: 0.580803 acc_val: 0.729730 time: 87.622521s
Epoch: 0021 loss_train: 1.188127 acc_train: 0.712360 loss_val: 0.575085 acc_val: 0.720721 time: 91.376217s
Epoch: 0022 loss_train: 1.196876 acc_train: 0.708989 loss_val: 0.580002 acc_val: 0.738739 time: 95.694479s
Epoch: 0023 loss_train: 1.174556 acc_train: 0.708989 loss_val: 0.601379 acc_val: 0.720721 time: 101.184839s
Epoch: 0024 loss_train: 1.184407 acc_train: 0.704494 loss_val: 0.580166 acc_val: 0.729730 time: 105.574432s
Epoch: 0025 loss_train: 1.207486 acc_train: 0.706742 loss_val: 0.579161 acc_val: 0.729730 time: 109.895133s
Epoch: 0026 loss_train: 1.195513 acc_train: 0.696629 loss_val: 0.581210 acc_val: 0.729730 time: 113.914422s
Epoch: 0027 loss_train: 1.176055 acc_train: 0.703371 loss_val: 0.575903 acc_val: 0.729730 time: 118.745483s
Epoch: 0028 loss_train: 1.182720 acc_train: 0.706742 loss_val: 0.581549 acc_val: 0.729730 time: 122.813510s
Epoch: 0029 loss_train: 1.171445 acc_train: 0.710112 loss_val: 0.565191 acc_val: 0.747748 time: 126.941170s
Epoch: 0030 loss_train: 1.176246 acc_train: 0.712360 loss_val: 0.562921 acc_val: 0.774775 time: 131.143402s
Epoch: 0031 loss_train: 1.175198 acc_train: 0.708989 loss_val: 0.573595 acc_val: 0.738739 time: 135.350930s
Epoch: 0032 loss_train: 1.162621 acc_train: 0.710112 loss_val: 0.564596 acc_val: 0.747748 time: 139.744460s
Epoch: 0033 loss_train: 1.166738 acc_train: 0.713483 loss_val: 0.571310 acc_val: 0.729730 time: 144.563742s
Epoch: 0034 loss_train: 1.178729 acc_train: 0.711236 loss_val: 0.566718 acc_val: 0.729730 time: 149.457201s
Epoch: 0035 loss_train: 1.160300 acc_train: 0.721348 loss_val: 0.567009 acc_val: 0.747748 time: 153.759484s
Epoch: 0036 loss_train: 1.162655 acc_train: 0.715730 loss_val: 0.578149 acc_val: 0.729730 time: 158.324167s
Epoch: 0037 loss_train: 1.159112 acc_train: 0.721348 loss_val: 0.560856 acc_val: 0.738739 time: 163.759796s
Epoch: 0038 loss_train: 1.151577 acc_train: 0.715730 loss_val: 0.562995 acc_val: 0.738739 time: 168.472944s
Epoch: 0039 loss_train: 1.149916 acc_train: 0.715730 loss_val: 0.563754 acc_val: 0.729730 time: 172.748666s
Epoch: 0040 loss_train: 1.150715 acc_train: 0.725843 loss_val: 0.555928 acc_val: 0.738739 time: 176.656028s
Epoch: 0041 loss_train: 1.152107 acc_train: 0.712360 loss_val: 0.565780 acc_val: 0.693694 time: 180.602279s
Epoch: 0042 loss_train: 1.145003 acc_train: 0.711236 loss_val: 0.556300 acc_val: 0.738739 time: 184.397899s
Epoch: 0043 loss_train: 1.149357 acc_train: 0.721348 loss_val: 0.573335 acc_val: 0.720721 time: 189.983971s
Epoch: 0044 loss_train: 1.144271 acc_train: 0.719101 loss_val: 0.560283 acc_val: 0.729730 time: 194.296131s
Epoch: 0045 loss_train: 1.128500 acc_train: 0.725843 loss_val: 0.558384 acc_val: 0.738739 time: 198.172704s
Epoch: 0046 loss_train: 1.132474 acc_train: 0.716854 loss_val: 0.560320 acc_val: 0.711712 time: 202.168023s
Epoch: 0047 loss_train: 1.146417 acc_train: 0.726966 loss_val: 0.562483 acc_val: 0.711712 time: 206.091612s
Epoch: 0048 loss_train: 1.145897 acc_train: 0.724719 loss_val: 0.556317 acc_val: 0.729730 time: 210.153487s
Epoch: 0049 loss_train: 1.124979 acc_train: 0.729213 loss_val: 0.557924 acc_val: 0.729730 time: 214.080156s
Epoch: 0050 loss_train: 1.140522 acc_train: 0.712360 loss_val: 0.565247 acc_val: 0.702703 time: 218.223837s
Epoch: 0051 loss_train: 1.130520 acc_train: 0.729213 loss_val: 0.559397 acc_val: 0.729730 time: 222.250009s
Epoch: 0052 loss_train: 1.127321 acc_train: 0.725843 loss_val: 0.570718 acc_val: 0.729730 time: 226.287270s
Epoch: 0053 loss_train: 1.151671 acc_train: 0.713483 loss_val: 0.563238 acc_val: 0.747748 time: 230.259609s
Epoch: 0054 loss_train: 1.156863 acc_train: 0.708989 loss_val: 0.558004 acc_val: 0.738739 time: 233.937465s
Epoch: 0055 loss_train: 1.126549 acc_train: 0.725843 loss_val: 0.609359 acc_val: 0.729730 time: 237.610236s
Epoch: 0056 loss_train: 1.151646 acc_train: 0.703371 loss_val: 0.556698 acc_val: 0.756757 time: 242.036500s
Epoch: 0057 loss_train: 1.160399 acc_train: 0.719101 loss_val: 0.551321 acc_val: 0.747748 time: 246.286753s
Epoch: 0058 loss_train: 1.142246 acc_train: 0.715730 loss_val: 0.586883 acc_val: 0.711712 time: 249.798076s
Epoch: 0059 loss_train: 1.142837 acc_train: 0.723596 loss_val: 0.556018 acc_val: 0.756757 time: 253.742087s
Epoch: 0060 loss_train: 1.132109 acc_train: 0.719101 loss_val: 0.556058 acc_val: 0.729730 time: 257.734007s
Epoch: 0061 loss_train: 1.122123 acc_train: 0.728090 loss_val: 0.558867 acc_val: 0.729730 time: 261.392365s
Epoch: 0062 loss_train: 1.111913 acc_train: 0.723596 loss_val: 0.555788 acc_val: 0.729730 time: 265.855547s
Epoch: 0063 loss_train: 1.104164 acc_train: 0.733708 loss_val: 0.561507 acc_val: 0.711712 time: 269.996811s
Epoch: 0064 loss_train: 1.113524 acc_train: 0.723596 loss_val: 0.554827 acc_val: 0.720721 time: 273.660656s
Epoch: 0065 loss_train: 1.103596 acc_train: 0.726966 loss_val: 0.556021 acc_val: 0.729730 time: 277.949159s
Epoch: 0066 loss_train: 1.105416 acc_train: 0.738202 loss_val: 0.556018 acc_val: 0.729730 time: 281.926837s
Epoch: 0067 loss_train: 1.135681 acc_train: 0.726966 loss_val: 0.555213 acc_val: 0.729730 time: 285.750334s
Epoch: 0068 loss_train: 1.116599 acc_train: 0.730337 loss_val: 0.549793 acc_val: 0.729730 time: 289.635071s
Epoch: 0069 loss_train: 1.114592 acc_train: 0.733708 loss_val: 0.553688 acc_val: 0.729730 time: 293.239839s
Epoch: 0070 loss_train: 1.111123 acc_train: 0.723596 loss_val: 0.567071 acc_val: 0.711712 time: 297.407959s
Epoch: 0071 loss_train: 1.113396 acc_train: 0.726966 loss_val: 0.555507 acc_val: 0.747748 time: 301.454265s
Epoch: 0072 loss_train: 1.100707 acc_train: 0.729213 loss_val: 0.558362 acc_val: 0.738739 time: 305.041150s
Epoch: 0073 loss_train: 1.121074 acc_train: 0.725843 loss_val: 0.549934 acc_val: 0.756757 time: 309.383266s
Epoch: 0074 loss_train: 1.089152 acc_train: 0.730337 loss_val: 0.544874 acc_val: 0.738739 time: 313.312231s
Epoch: 0075 loss_train: 1.094848 acc_train: 0.733708 loss_val: 0.564713 acc_val: 0.729730 time: 316.945816s
Epoch: 0076 loss_train: 1.098286 acc_train: 0.726966 loss_val: 0.551071 acc_val: 0.747748 time: 320.618745s
Epoch: 0077 loss_train: 1.096086 acc_train: 0.728090 loss_val: 0.552774 acc_val: 0.765766 time: 324.494982s
Epoch: 0078 loss_train: 1.092186 acc_train: 0.734831 loss_val: 0.551905 acc_val: 0.765766 time: 328.272420s
Epoch: 0079 loss_train: 1.101520 acc_train: 0.726966 loss_val: 0.549904 acc_val: 0.765766 time: 332.153932s
Epoch: 0080 loss_train: 1.097357 acc_train: 0.732584 loss_val: 0.547531 acc_val: 0.756757 time: 336.217810s
Epoch: 0081 loss_train: 1.111488 acc_train: 0.724719 loss_val: 0.546577 acc_val: 0.747748 time: 340.628776s
Epoch: 0082 loss_train: 1.098282 acc_train: 0.732584 loss_val: 0.565829 acc_val: 0.729730 time: 344.748131s
Epoch: 0083 loss_train: 1.099736 acc_train: 0.723596 loss_val: 0.554368 acc_val: 0.738739 time: 348.577461s
Epoch: 0084 loss_train: 1.096798 acc_train: 0.735955 loss_val: 0.555453 acc_val: 0.756757 time: 352.306713s
Epoch: 0085 loss_train: 1.093145 acc_train: 0.734831 loss_val: 0.548392 acc_val: 0.774775 time: 356.677878s
Epoch: 0086 loss_train: 1.089492 acc_train: 0.729213 loss_val: 0.544238 acc_val: 0.774775 time: 360.447610s
Epoch: 0087 loss_train: 1.106010 acc_train: 0.729213 loss_val: 0.545994 acc_val: 0.747748 time: 364.700011s
Epoch: 0088 loss_train: 1.108078 acc_train: 0.724719 loss_val: 0.550204 acc_val: 0.747748 time: 368.373518s
Epoch: 0089 loss_train: 1.092176 acc_train: 0.738202 loss_val: 0.548635 acc_val: 0.765766 time: 372.581709s
Epoch: 0090 loss_train: 1.079630 acc_train: 0.742697 loss_val: 0.562512 acc_val: 0.729730 time: 376.554642s
Epoch: 0091 loss_train: 1.085005 acc_train: 0.739326 loss_val: 0.545113 acc_val: 0.756757 time: 380.168732s
Epoch: 0092 loss_train: 1.092347 acc_train: 0.730337 loss_val: 0.546218 acc_val: 0.756757 time: 383.874550s
Epoch: 0093 loss_train: 1.088999 acc_train: 0.738202 loss_val: 0.546897 acc_val: 0.747748 time: 387.789865s
Epoch: 0094 loss_train: 1.087011 acc_train: 0.731461 loss_val: 0.541181 acc_val: 0.756757 time: 391.519451s
Epoch: 0095 loss_train: 1.087547 acc_train: 0.733708 loss_val: 0.550412 acc_val: 0.729730 time: 395.933904s
Epoch: 0096 loss_train: 1.084830 acc_train: 0.729213 loss_val: 0.545168 acc_val: 0.765766 time: 399.645914s
Epoch: 0097 loss_train: 1.085840 acc_train: 0.742697 loss_val: 0.549003 acc_val: 0.747748 time: 403.773188s
Epoch: 0098 loss_train: 1.079049 acc_train: 0.743820 loss_val: 0.539428 acc_val: 0.765766 time: 407.828803s
Epoch: 0099 loss_train: 1.096826 acc_train: 0.725843 loss_val: 0.535778 acc_val: 0.774775 time: 411.491378s
Epoch: 0100 loss_train: 1.083453 acc_train: 0.730337 loss_val: 0.539504 acc_val: 0.738739 time: 415.227974s
Epoch: 0101 loss_train: 1.076440 acc_train: 0.738202 loss_val: 0.534743 acc_val: 0.765766 time: 419.001498s
Epoch: 0102 loss_train: 1.075580 acc_train: 0.740449 loss_val: 0.546306 acc_val: 0.729730 time: 424.137055s
Epoch: 0103 loss_train: 1.069009 acc_train: 0.740449 loss_val: 0.536259 acc_val: 0.756757 time: 428.940894s
Epoch: 0104 loss_train: 1.072761 acc_train: 0.729213 loss_val: 0.536516 acc_val: 0.756757 time: 433.898081s
Epoch: 0105 loss_train: 1.073782 acc_train: 0.737079 loss_val: 0.544441 acc_val: 0.747748 time: 438.893707s
Epoch: 0106 loss_train: 1.078610 acc_train: 0.743820 loss_val: 0.538038 acc_val: 0.765766 time: 444.798897s
Epoch: 0107 loss_train: 1.068028 acc_train: 0.739326 loss_val: 0.545980 acc_val: 0.747748 time: 449.620727s
Epoch: 0108 loss_train: 1.072632 acc_train: 0.739326 loss_val: 0.537498 acc_val: 0.765766 time: 453.935729s
Epoch: 0109 loss_train: 1.076873 acc_train: 0.730337 loss_val: 0.536487 acc_val: 0.747748 time: 458.875587s
Epoch: 0110 loss_train: 1.063421 acc_train: 0.741573 loss_val: 0.553237 acc_val: 0.738739 time: 463.429392s
Epoch: 0111 loss_train: 1.053658 acc_train: 0.751685 loss_val: 0.543250 acc_val: 0.756757 time: 467.735300s
Epoch: 0112 loss_train: 1.080428 acc_train: 0.731461 loss_val: 0.545080 acc_val: 0.765766 time: 472.191656s
Epoch: 0113 loss_train: 1.062737 acc_train: 0.744944 loss_val: 0.544473 acc_val: 0.774775 time: 476.182014s
Epoch: 0114 loss_train: 1.039456 acc_train: 0.739326 loss_val: 0.543528 acc_val: 0.756757 time: 480.594454s
Epoch: 0115 loss_train: 1.068871 acc_train: 0.728090 loss_val: 0.540420 acc_val: 0.756757 time: 485.498450s
Epoch: 0116 loss_train: 1.064867 acc_train: 0.741573 loss_val: 0.538518 acc_val: 0.747748 time: 489.624120s
Epoch: 0117 loss_train: 1.071099 acc_train: 0.739326 loss_val: 0.537512 acc_val: 0.747748 time: 494.249886s
Epoch: 0118 loss_train: 1.060700 acc_train: 0.743820 loss_val: 0.556860 acc_val: 0.729730 time: 498.647860s
Epoch: 0119 loss_train: 1.067420 acc_train: 0.748315 loss_val: 0.538588 acc_val: 0.738739 time: 503.606132s
Epoch: 0120 loss_train: 1.061867 acc_train: 0.734831 loss_val: 0.542835 acc_val: 0.738739 time: 507.525245s
Epoch: 0121 loss_train: 1.050160 acc_train: 0.744944 loss_val: 0.540935 acc_val: 0.738739 time: 511.735065s
Epoch: 0122 loss_train: 1.063579 acc_train: 0.738202 loss_val: 0.538181 acc_val: 0.738739 time: 515.617908s
Epoch: 0123 loss_train: 1.053833 acc_train: 0.744944 loss_val: 0.542379 acc_val: 0.747748 time: 520.072780s
Epoch: 0124 loss_train: 1.048949 acc_train: 0.743820 loss_val: 0.535648 acc_val: 0.747748 time: 524.146967s
Epoch: 0125 loss_train: 1.060840 acc_train: 0.732584 loss_val: 0.555922 acc_val: 0.738739 time: 528.143851s
Epoch: 0126 loss_train: 1.061407 acc_train: 0.743820 loss_val: 0.542955 acc_val: 0.747748 time: 532.194831s
Epoch: 0127 loss_train: 1.055646 acc_train: 0.737079 loss_val: 0.545868 acc_val: 0.756757 time: 536.227782s
Epoch: 0128 loss_train: 1.056263 acc_train: 0.743820 loss_val: 0.550514 acc_val: 0.729730 time: 540.319492s
Epoch: 0129 loss_train: 1.029193 acc_train: 0.744944 loss_val: 0.543299 acc_val: 0.738739 time: 544.208170s
Epoch: 0130 loss_train: 1.048244 acc_train: 0.733708 loss_val: 0.559531 acc_val: 0.738739 time: 548.628795s
Epoch: 0131 loss_train: 1.041914 acc_train: 0.746067 loss_val: 0.547772 acc_val: 0.729730 time: 552.401468s
Epoch: 0132 loss_train: 1.047053 acc_train: 0.739326 loss_val: 0.550627 acc_val: 0.729730 time: 556.767972s
Epoch: 0133 loss_train: 1.050999 acc_train: 0.750562 loss_val: 0.551486 acc_val: 0.738739 time: 560.886922s
Epoch: 0134 loss_train: 1.041085 acc_train: 0.742697 loss_val: 0.542901 acc_val: 0.747748 time: 564.973189s
Epoch: 0135 loss_train: 1.035565 acc_train: 0.737079 loss_val: 0.554551 acc_val: 0.765766 time: 568.969738s
Epoch: 0136 loss_train: 1.040570 acc_train: 0.747191 loss_val: 0.545154 acc_val: 0.738739 time: 572.788154s
Epoch: 0137 loss_train: 1.090342 acc_train: 0.730337 loss_val: 0.551327 acc_val: 0.747748 time: 577.064010s
Epoch: 0138 loss_train: 1.083193 acc_train: 0.729213 loss_val: 0.549724 acc_val: 0.747748 time: 581.870309s
Epoch: 0139 loss_train: 1.042682 acc_train: 0.737079 loss_val: 0.544566 acc_val: 0.738739 time: 586.033723s
Epoch: 0140 loss_train: 1.043919 acc_train: 0.734831 loss_val: 0.573733 acc_val: 0.729730 time: 590.446674s
Epoch: 0141 loss_train: 1.049920 acc_train: 0.748315 loss_val: 0.543116 acc_val: 0.738739 time: 595.024223s
Epoch: 0142 loss_train: 1.061522 acc_train: 0.726966 loss_val: 0.543250 acc_val: 0.747748 time: 599.206688s
Epoch: 0143 loss_train: 1.015723 acc_train: 0.748315 loss_val: 0.578147 acc_val: 0.738739 time: 603.275177s
Epoch: 0144 loss_train: 1.027397 acc_train: 0.743820 loss_val: 0.546028 acc_val: 0.747748 time: 607.566344s
Epoch: 0145 loss_train: 1.050670 acc_train: 0.726966 loss_val: 0.551769 acc_val: 0.720721 time: 612.491326s
Epoch: 0146 loss_train: 1.042940 acc_train: 0.748315 loss_val: 0.563170 acc_val: 0.747748 time: 616.762033s
Epoch: 0147 loss_train: 1.021039 acc_train: 0.751685 loss_val: 0.544336 acc_val: 0.747748 time: 621.271802s
Epoch: 0148 loss_train: 1.041739 acc_train: 0.733708 loss_val: 0.559597 acc_val: 0.765766 time: 625.329072s
Epoch: 0149 loss_train: 1.042238 acc_train: 0.749438 loss_val: 0.545222 acc_val: 0.738739 time: 629.420970s
Epoch: 0150 loss_train: 1.026268 acc_train: 0.743820 loss_val: 0.546272 acc_val: 0.747748 time: 633.434351s
Epoch: 0151 loss_train: 1.032006 acc_train: 0.735955 loss_val: 0.576963 acc_val: 0.720721 time: 638.186262s
Epoch: 0152 loss_train: 1.025346 acc_train: 0.741573 loss_val: 0.542964 acc_val: 0.729730 time: 643.538887s
Epoch: 0153 loss_train: 1.027600 acc_train: 0.737079 loss_val: 0.538088 acc_val: 0.711712 time: 648.042440s
Epoch: 0154 loss_train: 1.018652 acc_train: 0.740449 loss_val: 0.575368 acc_val: 0.747748 time: 652.443031s
Epoch: 0155 loss_train: 1.007014 acc_train: 0.753933 loss_val: 0.549361 acc_val: 0.729730 time: 657.530985s
Epoch: 0156 loss_train: 1.001857 acc_train: 0.746067 loss_val: 0.544877 acc_val: 0.729730 time: 661.625972s
Epoch: 0157 loss_train: 1.010358 acc_train: 0.748315 loss_val: 0.557467 acc_val: 0.738739 time: 666.026773s
Epoch: 0158 loss_train: 1.003754 acc_train: 0.740449 loss_val: 0.541009 acc_val: 0.729730 time: 670.554416s
Epoch: 0159 loss_train: 0.993912 acc_train: 0.747191 loss_val: 0.556827 acc_val: 0.720721 time: 675.123185s
Epoch: 0160 loss_train: 1.001993 acc_train: 0.750562 loss_val: 0.551349 acc_val: 0.720721 time: 679.094252s
Epoch: 0161 loss_train: 0.983211 acc_train: 0.755056 loss_val: 0.544017 acc_val: 0.738739 time: 683.865851s
Epoch: 0162 loss_train: 0.991963 acc_train: 0.751685 loss_val: 0.554285 acc_val: 0.747748 time: 688.799439s
Epoch: 0163 loss_train: 0.988948 acc_train: 0.753933 loss_val: 0.556867 acc_val: 0.729730 time: 693.037739s
Epoch: 0164 loss_train: 0.976667 acc_train: 0.759551 loss_val: 0.548000 acc_val: 0.720721 time: 697.401802s
Epoch: 0165 loss_train: 0.986856 acc_train: 0.758427 loss_val: 0.560277 acc_val: 0.729730 time: 701.674442s
Epoch: 0166 loss_train: 0.989334 acc_train: 0.764045 loss_val: 0.556517 acc_val: 0.729730 time: 705.913666s
Epoch: 0167 loss_train: 0.982698 acc_train: 0.759551 loss_val: 0.563246 acc_val: 0.720721 time: 710.678619s
Epoch: 0168 loss_train: 0.984525 acc_train: 0.760674 loss_val: 0.568715 acc_val: 0.738739 time: 715.624716s
Epoch: 0169 loss_train: 0.984455 acc_train: 0.757303 loss_val: 0.558203 acc_val: 0.747748 time: 720.451542s
Epoch: 0170 loss_train: 0.987355 acc_train: 0.753933 loss_val: 0.560941 acc_val: 0.738739 time: 725.019700s
Epoch: 0171 loss_train: 0.980052 acc_train: 0.750562 loss_val: 0.563511 acc_val: 0.729730 time: 729.383049s
Epoch: 0172 loss_train: 0.970550 acc_train: 0.766292 loss_val: 0.557539 acc_val: 0.729730 time: 733.904813s
Epoch: 0173 loss_train: 0.974291 acc_train: 0.758427 loss_val: 0.569349 acc_val: 0.738739 time: 738.401191s
Epoch: 0174 loss_train: 0.974369 acc_train: 0.759551 loss_val: 0.563617 acc_val: 0.720721 time: 742.813065s
Epoch: 0175 loss_train: 1.019240 acc_train: 0.755056 loss_val: 0.600780 acc_val: 0.747748 time: 746.786930s
Epoch: 0176 loss_train: 1.008408 acc_train: 0.747191 loss_val: 0.546280 acc_val: 0.756757 time: 751.057233s
Epoch: 0177 loss_train: 1.027405 acc_train: 0.742697 loss_val: 0.547509 acc_val: 0.756757 time: 755.553156s
Epoch: 0178 loss_train: 0.995184 acc_train: 0.753933 loss_val: 0.584481 acc_val: 0.756757 time: 760.091932s
Epoch: 0179 loss_train: 0.986715 acc_train: 0.759551 loss_val: 0.544886 acc_val: 0.747748 time: 764.605619s
Epoch: 0180 loss_train: 0.994134 acc_train: 0.741573 loss_val: 0.574254 acc_val: 0.765766 time: 768.981267s
Epoch: 0181 loss_train: 0.995210 acc_train: 0.761798 loss_val: 0.546386 acc_val: 0.720721 time: 772.754442s
Epoch: 0182 loss_train: 0.972117 acc_train: 0.750562 loss_val: 0.538858 acc_val: 0.747748 time: 776.684755s
Epoch: 0183 loss_train: 0.977454 acc_train: 0.752809 loss_val: 0.590053 acc_val: 0.756757 time: 780.792241s
Epoch: 0184 loss_train: 0.992793 acc_train: 0.759551 loss_val: 0.556621 acc_val: 0.747748 time: 784.744471s
Epoch: 0185 loss_train: 1.026256 acc_train: 0.744944 loss_val: 0.552807 acc_val: 0.747748 time: 789.058596s
Epoch: 0186 loss_train: 1.004905 acc_train: 0.753933 loss_val: 0.584214 acc_val: 0.747748 time: 793.178921s
Epoch: 0187 loss_train: 0.990984 acc_train: 0.752809 loss_val: 0.534903 acc_val: 0.765766 time: 797.026792s
Epoch: 0188 loss_train: 0.991341 acc_train: 0.746067 loss_val: 0.563101 acc_val: 0.747748 time: 801.436227s
Epoch: 0189 loss_train: 0.976771 acc_train: 0.760674 loss_val: 0.571053 acc_val: 0.747748 time: 805.467620s
Epoch: 0190 loss_train: 0.974498 acc_train: 0.756180 loss_val: 0.562243 acc_val: 0.729730 time: 809.306529s
Epoch: 0191 loss_train: 0.965447 acc_train: 0.751685 loss_val: 0.568805 acc_val: 0.747748 time: 813.129113s
Epoch: 0192 loss_train: 0.968439 acc_train: 0.769663 loss_val: 0.555150 acc_val: 0.747748 time: 816.873454s
Epoch: 0193 loss_train: 0.957752 acc_train: 0.764045 loss_val: 0.573619 acc_val: 0.756757 time: 820.675056s
Epoch: 0194 loss_train: 0.962886 acc_train: 0.764045 loss_val: 0.570692 acc_val: 0.747748 time: 825.052693s
Epoch: 0195 loss_train: 0.950626 acc_train: 0.765169 loss_val: 0.556893 acc_val: 0.738739 time: 829.034768s
Epoch: 0196 loss_train: 0.964667 acc_train: 0.753933 loss_val: 0.586394 acc_val: 0.774775 time: 832.845055s
Epoch: 0197 loss_train: 0.970939 acc_train: 0.764045 loss_val: 0.575574 acc_val: 0.729730 time: 836.547364s
Epoch: 0198 loss_train: 0.954471 acc_train: 0.762921 loss_val: 0.561317 acc_val: 0.738739 time: 840.474387s
Epoch: 0199 loss_train: 0.951637 acc_train: 0.767416 loss_val: 0.577643 acc_val: 0.765766 time: 844.706279s
Epoch: 0200 loss_train: 0.968481 acc_train: 0.753933 loss_val: 0.577035 acc_val: 0.738739 time: 848.390988s
Epoch: 0201 loss_train: 0.949143 acc_train: 0.769663 loss_val: 0.589063 acc_val: 0.738739 time: 852.729391s
"""

# 将整个字符串按行拆分
lines = log_str.strip().split('\n')

epochs = []
loss_train = []
acc_train = []
loss_val = []
acc_val = []
times = []

for line in lines:
    # 使用正则表达式提取每一行中的数据
    match = re.search(r'Epoch: (\d+) loss_train: ([\d.]+) acc_train: ([\d.]+) loss_val: ([\d.]+) acc_val: ([\d.]+) time: ([\d.]+)s', line)
    if match:
        epochs.append(int(match.group(1)))
        loss_train.append(float(match.group(2)))
        acc_train.append(float(match.group(3)))
        loss_val.append(float(match.group(4)))
        acc_val.append(float(match.group(5)))
        times.append(float(match.group(6)))

plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.plot(epochs, loss_train, label='Training Loss')
plt.plot(epochs, loss_val, label='Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.title('Training and Validation Loss')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(epochs, acc_train, label='Training Accuracy')
plt.plot(epochs, acc_val, label='Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.title('Training and Validation Accuracy')
plt.legend()

plt.show()