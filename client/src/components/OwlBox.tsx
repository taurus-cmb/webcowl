import React from "react";
import { Heading, Card, CardBody, Center, Table, TableContainer, Tbody } from "@chakra-ui/react";

export function OwlBox({
  header,
  bg,
  children,
}: {
  header: string;
  bg?: string;
  children?: React.ReactNode;
}) {
  // TODO Use CardHeader for Heading? (would need to fix padding)
  return (
    <Card bg={bg}>
      <CardBody>
        <Center>
          <Heading as="h3" size="m">
            {header}
          </Heading>
        </Center>
        <TableContainer>
          <Table variant="unstyled">
            <Tbody>{children}</Tbody>
          </Table>
        </TableContainer>
      </CardBody>
    </Card>
  );
}
