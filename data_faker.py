import pygetdata as gd
import time
import os
import random
import numpy as np

output_path = os.path.join(os.path.dirname(__file__), "fake_data")
update_period = 0.5

# create dirfile and add fields
df = gd.dirfile(output_path, gd.RDWR | gd.CREAT | gd.TRUNC)
for field in ["TIME", "NOISE", "STEPPY"]:
    df.add(gd.entry(gd.RAW_ENTRY, field, fragment_index=0, parameters=dict(type=gd.FLOAT64, spf=1)))
df.flush()

# initial conditions
start_time = time.time()
count = 0

print(f"Writing fake data to: {output_path}")

# main loop
try:
    while True:
        # update the time
        current_time = time.time()
        df.putdata("TIME", [current_time], first_sample=count)
        # update the field that is just noise
        noise_data = random.normalvariate(mu=0, sigma=1)
        df.putdata("NOISE", [noise_data], first_sample=count)
        # update the field that is noise plus a square wave
        steppy_data = random.normalvariate(mu=0, sigma=1)
        # step for 3 seconds out of every 10
        if current_time % 10 < 3:
            steppy_data += 20
        df.putdata("STEPPY", [steppy_data], first_sample=count)

        count += 1
        time.sleep(update_period)
except KeyboardInterrupt:
    print("Stopping data faker")
finally:
    df.close()
