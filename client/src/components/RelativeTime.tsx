import { useState, useEffect } from "react";

function get_relative_date_string(date: Date): [string, number] {
  const formatter = new Intl.RelativeTimeFormat("en");
  const ranges = {
    years: 3600 * 24 * 365,
    months: 3600 * 24 * 30,
    weeks: 3600 * 24 * 7,
    days: 3600 * 24,
    hours: 3600,
    minutes: 60,
    seconds: 1,
  };
  const secondsElapsed = (date.getTime() - Date.now()) / 1000;
  let key: keyof typeof ranges;
  for (key in ranges) {
    if (ranges[key] < Math.abs(secondsElapsed)) {
      const delta = secondsElapsed / ranges[key];
      const relativeString = formatter.format(Math.round(delta), key);
      // update after half of unit, but not longer than 2 minutes
      const updateSeconds = Math.min(ranges[key] / 2, 120);
      return [relativeString, updateSeconds];
    }
  }
  return ["now", 0.5];
}

export function RelativeTime({ date }: { date: Date }) {
  const [relativeString, updateSeconds] = get_relative_date_string(date);
  const [, setUpdate] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => setUpdate((update) => update + 1), updateSeconds * 1000);
    return () => clearInterval(timer);
  }, [updateSeconds]);

  return <>{relativeString}</>;
}
