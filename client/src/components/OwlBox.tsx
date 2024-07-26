import React from 'react'
import { VStack, SimpleGrid, Heading } from '@chakra-ui/react'

export function OwlBox({ bg, header, children }: { bg: string, header: string, children?: React.ReactNode }) {
  // TODO maybe build around Table instead?
  return (
    <VStack bg={bg} p={4} spacing={1}>
      <Heading as="h3" size="m">{header}</Heading>
      <SimpleGrid columns={2} columnGap={4}>
        {children}
      </SimpleGrid>
    </VStack>
  )
}


