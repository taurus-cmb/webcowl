import { Text, Tr, Td } from "@chakra-ui/react";
import { useSharedData, DataType } from "../contexts/SharedDataProvider";
import { RelativeTime } from "./RelativeTime";

/**
 * Format value to a date, assuming C/UNIX time in seconds
 *
 * @param value The time in seconds
 *
 * @returns A string representing the time
 */
export function format_date(value: number) {
  // Date wants milliseconds
  return new Date(value * 1000).toLocaleString();
}

/**
 * Format value to a relative time interval, assuming C/UNIX time in seconds
 *
 * @param value The time in seconds
 *
 * @returns A RelativeTime component that shows the time and updates
 */
export function format_date_relative(value: number) {
  // Date wants milliseconds
  const date = new Date(value * 1000);
  return <RelativeTime date={date} />;
}

/**
 * Formatter factory function for numbers, given number of decimal places.
 *
 * @param decimals The number of  decimal points to show
 * @param [options={}] other options for toLocaleString
 *
 * @returns A string representing the time relative to now
 */
export function format_number(decimals: number, options = {}) {
  return (val: number) =>
    val.toLocaleString(undefined, {
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals,
      ...options,
    });
}

const format_default = (val: number) => String(val);

// Wrap the formatter function, handling special cases when either
// data doesn't exist, or doesn't include desired field
function format_wrapper(data: DataType, field: string, formatter: Function) {
  if (data === undefined) {
    // no data has been received
    return "Load";
  } else {
    const val = data[field];
    if (val === undefined) {
      // data received, but doesn't contain this field
      return "undefined";
    }
    return formatter(val);
  }
}

export function OwlValue({
  label,
  field,
  formatter = format_default,
}: {
  label: string;
  field: string;
  formatter: Function;
}) {
  const { data } = useSharedData(field);

  return (
    <Tr>
      <Td p={1}>
        <Text>{label}</Text>
      </Td>
      <Td p={1}>
        <Text>{format_wrapper(data, field, formatter)}</Text>
      </Td>
    </Tr>
  );
}
