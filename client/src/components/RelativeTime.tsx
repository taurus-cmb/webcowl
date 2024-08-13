import { useState, useEffect } from "react";

function get_relative_date_string(date: Date): [string, number] {
  const formatter = new Intl.RelativeTimeFormat("en");
  const ranges: { unit: Intl.RelativeTimeFormatUnit; len: number; step: number }[] = [
    { unit: "years", len: 3600 * 24 * 365, step: 1 },
    { unit: "months", len: 3600 * 24 * 30, step: 1 },
    { unit: "weeks", len: 3600 * 24 * 7, step: 1 },
    { unit: "days", len: 3600 * 24, step: 1 },
    { unit: "hours", len: 3600, step: 1 },
    { unit: "minutes", len: 60, step: 5 },
    { unit: "minutes", len: 60, step: 1 },
    { unit: "seconds", len: 1, step: 5 },
  ];
  const secondsElapsed = (date.getTime() - Date.now()) / 1000;
  for (const idx in ranges) {
    const { unit, len, step } = ranges[idx];
    const total_len = len * step;
    if (total_len < Math.abs(secondsElapsed)) {
      const delta = secondsElapsed / total_len;
      // always round towards zero
      // instead of floor that rounds negative numbers further from zero
      const rounded = Math.sign(delta) * Math.floor(Math.abs(delta)) * step;
      const relativeString = formatter.format(rounded, unit);
      // update after half of unit, but not longer than 2 minutes
      const updateSeconds = Math.min(len / 2, 120);
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
