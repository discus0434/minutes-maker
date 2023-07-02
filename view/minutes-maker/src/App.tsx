import { useState } from "react";
import "./App.css";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import { FileUploader } from "./Components/FileUploader";
import { ResultDisplay } from "./Components/ResultDisplay";
import { AppContext } from "./Components/AppContext";
import { ApiResponseDataSchema } from "./Components/ApiResponseDataSchema";
import { Title } from "./Components/Title";

function App() {
  const [apiResponse, setApiResponse] = useState<ApiResponseDataSchema | null>(
    null
  );
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const theme = createTheme({
    palette: {
      primary: {
        // Purple and green play nicely together.
        main: "#5c6bc0",
      },
      secondary: {
        // This is green.A700 as hex.
        main: "#11cb5f",
      },
    },
  });

  return (
    <AppContext.Provider value={{ apiResponse, isLoading }}>
      <ThemeProvider theme={theme}>
        <div className="App">
          <Title />
          <FileUploader
            setApiResponse={setApiResponse}
            setIsLoading={setIsLoading}
          />
          <ResultDisplay />
        </div>
      </ThemeProvider>
    </AppContext.Provider>
  );
}

export default App;
