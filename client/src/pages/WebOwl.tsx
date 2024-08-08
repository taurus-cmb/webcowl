import { HStack } from "@chakra-ui/react";
import { OwlBox } from "../components/OwlBox";
import { OwlValue, format_date, format_number } from "../components/OwlValue";
import { SharedDataProvider } from "../contexts/SharedDataProvider";

export function WebOwl() {
  return (
    <SharedDataProvider>
      <HStack spacing={4}>
        <OwlBox header="Test Data">
          <OwlValue label="Time" field="TIME" formatter={format_date} />
          <OwlValue label="Noise" field="NOISE" formatter={format_number(2)} />
          <OwlValue label="Steppy" field="STEPPY" formatter={format_number(2)} />
          <OwlValue label="Bad name" field="BAD_NAME" formatter={format_number(3)} />
        </OwlBox>
      </HStack>
    </SharedDataProvider>
  );
}
