import { createContext, useContext, useState, useCallback, ReactNode } from "react"

const defaultValue = {
  addField: (_: string) => { return },
}

// FIXME missing default value, something better than empty object?
const sharedDataContext = createContext(defaultValue)

export function SharedDataProvider({ children }: { children: ReactNode}) {
  const [fields, setFields] = useState(new Set(["INDEX"]));  

  function addField(field: string) {
    if (!fields.has(field)) {
      let newFields = new Set(fields)
      newFields.add(field)
      setFields(newFields)
    }
  }

  return (
    <sharedDataContext.Provider value={{addField}}>
      <p>Test: [{new Array(fields)}]</p>
      { children }
    </sharedDataContext.Provider>
  )
}

export function useSharedData() {
  return useContext(sharedDataContext)
}
