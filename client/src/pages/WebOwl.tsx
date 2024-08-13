import { HStack } from "@chakra-ui/react";
import { OwlBox } from "../components/OwlBox";
import { OwlValue, format_date, format_date_relative, format_number } from "../components/OwlValue";
import { SharedDataProvider } from "../contexts/SharedDataProvider";
import { StyleLimits } from "../components/StyleLimits";

let limits = new StyleLimits(
  { xlo: -10, lo: -2, hi: 2, xhi: 10 },
  {
    xlo: { bg: "green.300", fontWeight: "bold" },
    lo: { color: "green.600", fontWeight: "bold" },
    hi: { color: "red.600", fontWeight: "bold" },
    xhi: { bg: "red.300", fontWeight: "bold" },
  },
);

export function WebOwl() {
  return (
    <SharedDataProvider>
      <HStack spacing={4}>
        <OwlBox header="Test Data">
          <OwlValue label="Time" field="TIME" formatter={format_date} />
          <OwlValue label="...rel" field="TIME" formatter={format_date_relative} />
          <OwlValue label="Noise" field="NOISE" limits={limits} formatter={format_number(2)} />
          <OwlValue label="Steppy" field="STEPPY" limits={limits} formatter={format_number(2)} />
          <OwlValue
            label="Bad name"
            field="BAD_NAME"
            limits={limits}
            formatter={format_number(3)}
          />
        </OwlBox>
      </HStack>
    </SharedDataProvider>
  );
}
