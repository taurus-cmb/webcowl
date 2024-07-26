import React from 'react'
import { Heading, Card, CardBody, Center, Table, TableContainer } from '@chakra-ui/react'

export function OwlBox({ bg, header, children }: { bg: string, header: string, children?: React.ReactNode }) {
  // TODO Use CardHeader for Heading? (would need to fix padding)
  return (
    <Card bg={bg}>
      <CardBody>
        <Center><Heading as="h3" size="m">{header}</Heading></Center>
        <TableContainer>
          <Table variant="unstyled">
            {children}
          </Table>
        </TableContainer>
      </CardBody>
    </Card>
  )
}


