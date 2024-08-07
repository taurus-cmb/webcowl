import { createContext, useContext, useState, ReactNode, useEffect } from "react"
import { useQuery } from '@tanstack/react-query'
import { Text } from "@chakra-ui/react"

const defaultValue = {
  addField: (_: string) => { return },
  fields: new Set(["INDEX"]),
  isLoading: true,
  isError: false,
  data: {}, //new Map(),
  error: null as Error | null,
}

const sharedDataContext = createContext(defaultValue)

export function SharedDataProvider({ children }: { children: ReactNode }) {
  const [fields, setFields] = useState(new Set(["INDEX"]));

  function addField(field: string) {
    if (!fields.has(field)) {
      let newFields = new Set(fields)
      newFields.add(field)
      setFields(newFields)
    }
  }

  async function dataQuery() {
    const fieldsObject = { fields: new Array(...fields) }
    const response = await fetch("/api/latest", {
      // learn more about this API here: https://graphql-pokemon2.vercel.app/
      method: 'POST',
      headers: {
        'content-type': 'application/json;charset=UTF-8',
      },
      body: JSON.stringify(fieldsObject),
    })

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

  const { isLoading, isError, data, error } = useQuery({
    queryKey: ["api_test"],
    queryFn: dataQuery,
    refetchInterval: 2000,
  });


  // when return a map, it can be undefined. create a special map for that case
  // let data_def = data;
  // if (data_def === undefined) {
  //   data_def = new Map([["INDEX", -1]])
  // }


  return (
    <sharedDataContext.Provider value={{addField, fields, isLoading, isError, data, error}}>
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
  // TODO this might be O(N^2), but seems fine for now, and only happens once
  useEffect(() => {context.addField(field)}, [field, context.fields])
  return context
}
