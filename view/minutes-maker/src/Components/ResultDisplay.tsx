import React, { useContext } from "react";
import { AppContext } from "./AppContext";
import ReactMarkdown from "react-markdown";
import { Box, Paper, Typography } from "@mui/material";
import PacmanLoader from "react-spinners/PacmanLoader";

// This component receives two texts from a REST API and displays them side by side
const ResultDisplay: React.FC = () => {
  const { apiResponse, isLoading } = useContext(AppContext);

  // if apiResponse is null, return null
  return isLoading ? (
    apiResponse ? (
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          flexWrap: "wrap",
          mt: 2,
          mx: "auto",
          width: "98%",
        }}
      >
        {/* animate shadow when hover */}
        <Paper
          sx={{
            width: { xs: "100%", md: "45%" },
            padding: 3,
            margin: 1,
            textAlign: "left",
            backgroundColor: "#f6f6f6",
            boxShadow: "0px 0px 8px rgba(0, 0, 0, 0.12)",
            "&:hover": {
              boxShadow: "0px 0px 8px 2px rgba(9, 67, 68, 0.23)",
            },
          }}
        >
          <Typography
            variant="h4"
            sx={{
              fontWeight: "bold",
              color: "primary.main",
              fontFamily: "Ubuntu",
            }}
          >
            Timeline
          </Typography>
          <ReactMarkdown children={apiResponse.timeline} />
        </Paper>
        <Paper
          sx={{
            width: { xs: "100%", md: "45%" },
            padding: 3,
            margin: 1,
            textAlign: "left",
            backgroundColor: "#f6f6f6",
            boxShadow: "0px 0px 8px rgba(0, 0, 0, 0.12)",
            "&:hover": {
              boxShadow: "0px 0px 8px 2px rgba(9, 67, 68, 0.23)",
            },
          }}
        >
          <Typography
            variant="h4"
            sx={{
              fontWeight: "bold",
              color: "primary.main",
              fontFamily: "Ubuntu",
            }}
          >
            Summary
          </Typography>
          <ReactMarkdown children={apiResponse.summary} />
        </Paper>
      </Box>
    ) : (
      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          height: "50vh",
        }}
      >
        <PacmanLoader color="#5c6bc0" loading={true} size={20} />
      </Box>
    )
  ) : null;
};

export { ResultDisplay };
