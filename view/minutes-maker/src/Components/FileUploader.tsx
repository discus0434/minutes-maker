import React, { useState } from "react";
import axios from "axios";
import { ApiResponseDataSchema } from "./ApiResponseDataSchema";
import {
  Box,
  Button,
  FormControl,
  FormControlLabel,
  FormLabel,
  TextField,
  Radio,
  RadioGroup,
} from "@mui/material";

interface FileUploaderProps {
  setApiResponse: React.Dispatch<
    React.SetStateAction<ApiResponseDataSchema | null>
  >;
  setIsLoading: React.Dispatch<React.SetStateAction<boolean>>;
}

// This component accepts a file and a content as input and sends them to a REST API
const FileUploader: React.FC<FileUploaderProps> = ({
  setApiResponse,
  setIsLoading,
}) => {
  const [file, setFile] = useState<File | null>(null);
  const [language, setLanguage] = useState<string>("ja"); // default: ja
  const [category, setCategory] = useState<string>("meeting");
  const [content, setContent] = useState<string>("");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFile(e.target.files ? e.target.files[0] : null);
  };

  const handleLanguageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setLanguage(e.target.value);
  };

  const handleCategoryChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setCategory(e.target.value);
  };

  const handleContentChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setContent(e.target.value);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (file && language && category && content) {
      setIsLoading(true); // Set isLoading to true
      setApiResponse(null); // Reset the API response
      const formData = new FormData(); // Create a new FormData instance
      formData.append("file", file); // Append the file
      formData.append("filename", file.name); // Append the filename
      formData.append("language", language); // Append the language
      formData.append("category", category); // Append the audio type
      formData.append("content", content); // Append the content

      await axios
        .post(`http://${process.env.REACT_APP_PUBLIC_IP!}:10355/minutes_maker`, formData)
        .then((response) => {
          setApiResponse(response.data); // Store the API response in state
        })
        .catch((error) => {
          console.log(error);
        });
    } else {
      console.log("file or content is null");
    }
  };

  return (
    <Box
      component="form"
      onSubmit={handleSubmit}
      noValidate
      sx={{
        width: "40%",
        margin: "auto",
        textAlign: "center",
        mt: 4,
        padding: 4,
        backgroundColor: "#f6f6f6",
        boxShadow: "0px 0px 8px rgba(0, 0, 0, 0.12)",
        borderRadius: 2,
      }}
    >
      {/* file input */}
      <FormLabel
        component="legend"
        sx={{
          fontWeight: "bold",
          color: "primary.main",
          fontFamily: "Ubuntu",
          mb: 2,
        }}
      >
        1. Upload audio or video file
      </FormLabel>
      <TextField
        variant="outlined"
        required
        fullWidth
        name="file"
        type="file"
        id="file"
        onChange={handleFileChange}
        helperText="e.g. mp3, mp4, m4a, etc."
      />
      {/* radio buttons for target language (options: ja or en) */}
      <Box sx={{ mb: 1 }}>
        <FormControl sx={{ mb: 1 }}>
          <FormLabel
            component="legend"
            sx={{
              fontWeight: "bold",
              color: "primary.main",
              fontFamily: "Ubuntu",
            }}
          >
            2. Select target language
          </FormLabel>
          <RadioGroup
            row
            aria-label="language"
            name="language"
            value={language}
            onChange={handleLanguageChange}
            sx={{
              border: "1.5px solid #d9d9d9",
              borderRadius: 2,
              mt: 2,
              p: 1,
              paddingLeft: 2,
            }}
          >
            <FormControlLabel value="ja" control={<Radio />} label="Japanese" />
            <FormControlLabel value="en" control={<Radio />} label="English" />
          </RadioGroup>
        </FormControl>
      </Box>
      {/* radio buttons for category (options: meeting or lecture) */}
      <Box sx={{ mb: 1 }}>
        <FormControl sx={{ marginBottom: 1 }}>
          <FormLabel
            component="legend"
            sx={{
              fontWeight: "bold",
              color: "primary.main",
              fontFamily: "Ubuntu",
            }}
          >
            3. Select category
          </FormLabel>
          <RadioGroup
            row
            aria-label="category"
            name="category"
            value={category}
            onChange={handleCategoryChange}
            sx={{
              border: "1.5px solid #d9d9d9",
              borderRadius: 2,
              mt: 2,
              p: 1,
              paddingLeft: 2,
            }}
          >
            <FormControlLabel
              value="meeting"
              control={<Radio />}
              label="Meeting"
            />
            <FormControlLabel
              value="lecture"
              control={<Radio />}
              label="Lecture"
            />
          </RadioGroup>
        </FormControl>
      </Box>
      {/* text input for content(topic) */}
      <FormLabel
        component="legend"
        sx={{ fontWeight: "bold", color: "primary.main", fontFamily: "Ubuntu" }}
      >
        4. Enter meeting/lecture topic
      </FormLabel>
      <TextField
        variant="outlined"
        margin="normal"
        required
        fullWidth
        id="content"
        label="Content"
        name="content"
        autoComplete="content"
        autoFocus
        value={content}
        onChange={handleContentChange}
        helperText="e.g. AI, 商品開発, etc."
        sx={{ marginBottom: 2 }}
      />
      <Button
        type="submit"
        fullWidth
        variant="contained"
        color="primary"
        sx={{
          mt: 2,
          mb: 2,
          p: 1,
          fontFamily: "Ubuntu",
          width: "50%",
          margin: "auto",
          "&:hover": {
            backgroundColor: "#009688",
            shadow: "0px 0px 8px 2px rgba(9, 67, 68, 0.4)",
          },
        }}
      >
        Submit! (takes a few minutes)
      </Button>
    </Box>
  );
};

export { FileUploader };
