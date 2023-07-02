import { Typography } from "@mui/material";

const Title: React.FC = () => {
  return (
    <Typography
      variant="h2"
      gutterBottom
      component="div"
      sx={{
        fontFamily: "Ubuntu",
        marginTop: 3,
        marginBottom: 1,
        fontWeight: "bold",
        color: "primary.main",
      }}
    >
      Minutes Maker
    </Typography>
  );
};

export { Title };
