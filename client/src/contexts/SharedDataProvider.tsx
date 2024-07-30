import { createContext, useContext, useState, ReactNode } from "react"
import { useQuery } from '@tanstack/react-query'
import { Text } from "@chakra-ui/react"

const defaultValue = {
  addField: (_: string) => { return },
  isLoading: true,
  isError: false,
  data: {}, //new Map(),
  error: null as Error | null,
}

const sharedDataContext = createContext(defaultValue)

async function dataQuery() {
      const response = await fetch("/api/test")
      if (!response.ok) {
        const text = await response.text()
        throw new Error("Error: " + text)
      }
      const obj = response.json()
      // FIXME when returning a map, always get undefined values
      // properties of obj depend on requested fields
      // to be more typescript friendly, return a Map instead
      //return new Map<string, number>(Object.entries(obj))
      return obj
  }

export function SharedDataProvider({ children }: { children: ReactNode}) {
  const [fields, setFields] = useState(new Set(["INDEX"]));  

  function addField(field: string) {
    if (!fields.has(field)) {
      let newFields = new Set(fields)
      newFields.add(field)
      setFields(newFields)
    }
  }

  const { isLoading, isError, data, error } = useQuery({
    queryKey: ["api_test"],
    queryFn: dataQuery,
    refetchInterval: 500,
  });


  // when return a map, it can be undefined. create a special map for that case
  // let data_def = data;
  // if (data_def === undefined) {
  //   data_def = new Map([["INDEX", -1]])
  // }


  return (
    <sharedDataContext.Provider value={{addField, isLoading, isError, data, error}}>
      <Text>Test: [{new Array(fields)}]</Text>
      <Text>
        Data status: {isLoading ? "Loading..." : isError ? "Error: " + error : "Loaded index: " + data["INDEX"]}
      </Text>
      { children }
    </sharedDataContext.Provider>
  )
}

export function useSharedData(field: string) {
  let context = useContext(sharedDataContext)
  // FIXME this causes a warning about updating SharedDataProvider while rendering OwlValue
  context.addField(field)
  return context
}
