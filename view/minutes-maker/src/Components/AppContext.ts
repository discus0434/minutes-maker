import { createContext } from "react";
import { ApiResponseDataSchema } from "./ApiResponseDataSchema";

interface AppContextProps {
  apiResponse: ApiResponseDataSchema | null;
  isLoading: boolean;
}

// Create a context to store the API response data and the loading state
const AppContext = createContext<AppContextProps>({
  apiResponse: null,
  isLoading: false,
});

export { AppContext };
