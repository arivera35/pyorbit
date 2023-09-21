import ephem
from sgp4.earth_gravity import wgs84
from sgp4.io import twoline2rv, verify_checksum, fix_checksum

tle1 = []
tle1.append("1 99998U       16033.50000000 -.00000082  00000-0 -21065-5 0 00007") 
tle1.append("2 99998       055.0190 359.9965 0008971 268.7611 091.2409 15.38670435000017")
print(type(tle1))
# ("1 99998U 16033.50000000 -.00000082  00000-0 -21065-5 0 00007",
#         "2 99998 055.0190 359.9965 0008971 268.7611 091.2409 15.38670435000017")

# tle2 = ("1 99997U 16033.50000000 -.00000327  00000-0 -81943-5 0 00000",
        # "2 99997 045.0203 000.0034 0007772 267.0094 092.9891 15.39231281000013")
print(fix_checksum(tle1[0]))
print(fix_checksum(tle1[1]))
tle1_fixed = (fix_checksum(tle1[0]), fix_checksum(tle1[1]))
# tle2_fixed = (fix_checksum(tle2[0]), fix_checksum(tle2[1]))

sat1 = ephem.readtle("TEST", tle1_fixed[0], tle1_fixed[1])
# sat2 = ephem.readtle("TEST", tle2_fixed[0], tle2_fixed[1])

for tle in [tle1_fixed]:
    for line in tle:
        verify_checksum(line)

# print(tle1_fixed)
# print(tle2_fixed)

print(sat1)
# print(sat2)