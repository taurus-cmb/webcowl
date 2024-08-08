import { Text, Tr, Td } from "@chakra-ui/react";
import { useSharedData } from "../contexts/SharedDataProvider";

export function format_date(value: number) {
  return new Date(value * 1000).toLocaleString();
}

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
// FIXME make data not any type
function format_wrapper(data: any, field: string, formatter: Function) {
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
