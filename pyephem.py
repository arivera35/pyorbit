import ephem

# Create an observer for your location (latitude, longitude, elevation in meters)
observer = ephem.Observer()
observer.lat = '31.767600'
observer.lon = '-106.43502'

# Create a satellite object (TLE data for ISS)
tle_line1 = "1 25544U 98067A   23234.68087506  .00013766  00000+0  25254-3 0  9997"
tle_line2 = "2 25544  51.6416 359.1297 0003725 336.6499 154.9515 15.49565710412109"
satellite = ephem.readtle("ISS (ZARYA)", tle_line1, tle_line2)

# Calculate and print the next pass of the ISS for your location
next_pass = observer.next_pass(satellite)
print("Next ISS pass:")
print("Rise time:", next_pass[0])
print("Set time:", next_pass[2])
