import { useState, useEffect } from "react";

function get_relative_date_string(date: Date): [string, number] {
  const formatter = new Intl.RelativeTimeFormat("en");
  const ranges: { unit: Intl.RelativeTimeFormatUnit; len: number; mult: number }[] = [
    { unit: "years", len: 3600 * 24 * 365, mult: 1 },
    { unit: "months", len: 3600 * 24 * 30, mult: 1 },
    { unit: "weeks", len: 3600 * 24 * 7, mult: 1 },
    { unit: "days", len: 3600 * 24, mult: 1 },
    { unit: "hours", len: 3600, mult: 1 },
    { unit: "minutes", len: 60 * 5, mult: 5 },
    { unit: "minutes", len: 60, mult: 1 },
    { unit: "seconds", len: 5, mult: 5 },
  ];
  const secondsElapsed = (date.getTime() - Date.now()) / 1000;
  for (const idx in ranges) {
    const { unit, len, mult } = ranges[idx];
    if (len < Math.abs(secondsElapsed)) {
      const delta = secondsElapsed / len;
      // always round towards zero
      // instead of floor that rounds negative numbers further from zero
      const rounded = Math.sign(delta) * Math.floor(Math.abs(delta)) * mult;
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
