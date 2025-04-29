import time
import os
import random

# initial conditions
start_time = time.time()
update_period = 0.5

def simulate_index(t):
    return int((t - start_time) / update_period)

# functions that simulate the data
def simulate_time(t):
    return t

def simulate_noise(t):
    return random.normalvariate(mu=0, sigma=1)

def simulate_steppy_noise(t):
    val = random.normalvariate(mu=0, sigma=1)
    # step by 20 for 3 out of every 10 seconds
    if t % 10 < 3:
        val += 20
    return val

def simulate_triangle_data(t):
    return (t % 10 - 5) * 3


fake_data_fields = {
    "TIME": simulate_time,
    "NOISE": simulate_noise,
    "STEPPY": simulate_steppy_noise,
    "TRIANGLE": simulate_triangle_data,
}

# function that can be called from API server to simulate data without dirfile
def get_fake_data(fields):
    result = {}
    current_time = time.time()
    result["INDEX"] = simulate_index(current_time)
    for field in fields:
        if field in fake_data_fields:
            result[field] = fake_data_fields[field](current_time)
    return result


if __name__ == "__main__":
    # when running directly, write values to a dirfile
    import pygetdata as gd

    output_path = os.path.join(os.path.dirname(__file__), "fake_data")

    # create dirfile and add fields
    df = gd.dirfile(output_path, gd.RDWR | gd.CREAT | gd.TRUNC)
    for field in fake_data_fields:
        df.add(gd.entry(gd.RAW_ENTRY, field, fragment_index=0, parameters=dict(type=gd.FLOAT64, spf=1)))
    df.flush()

    print(f"Writing fake data to: {output_path}")

    # main loop
    try:
        count = 0
        while True:
            current_time = time.time()
            for field, func in fake_data_fields.items():
                val = func(current_time)
                df.putdata(field, [val], first_sample=count)
            count += 1
            time.sleep(update_period)
    except KeyboardInterrupt:
        print("Stopping data faker")
    finally:
        df.close()
