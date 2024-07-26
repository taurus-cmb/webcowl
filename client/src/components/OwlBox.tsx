import React from 'react'
import { SimpleGrid, Heading, Card, CardBody,Center } from '@chakra-ui/react'

export function OwlBox({ bg, header, children }: { bg: string, header: string, children?: React.ReactNode }) {
  // TODO maybe build around Table instead?
  // TODO Use CardHeader for Heading? (would need to fix padding)
  return (
    <Card bg={bg}>
      <CardBody>
        <Center><Heading as="h3" size="m">{header}</Heading></Center>
        <SimpleGrid columns={2} columnGap={4}>
          {children}
        </SimpleGrid>
      </CardBody>
    </Card>
  )
}


