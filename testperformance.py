import React, { useEffect, useState, useContext, useMemo } from "react";
import {
  getPerformance,
  addPerformance,
  updatePerformance,
  deletePerformance,
  getProfiles,
} from "../api";
import { AuthContext } from "./AuthContext";
import {
  Box,
  Card,
  CardContent,
  TextField,
  Button,
  MenuItem,
  Select,
  InputLabel,
  FormControl,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
} from "@mui/material";
import "../pages/css/global.css";

const Performance = () => {
  const { user } = useContext(AuthContext);
  const [performances, setPerformances] = useState([]);
  const [profiles, setProfiles] = useState([]);
  const [formData, setFormData] = useState({
    userId: "",
    score: "",
    remarks: "",
  });

  const isAdmin = user?.role === "admin";

  // Fetch performances and profiles
  useEffect(() => {
    if (!user?.profile) return;

    const fetchData = async () => {
      try {
        const [perfRes, profileRes] = await Promise.all([
          getPerformance(user.profile),
          getProfiles(user.profile),
        ]);
        setPerformances(perfRes.data || perfRes);
        setProfiles(profileRes.data || profileRes);
      } catch (err) {
        console.error("Data fetch error:", err);
      }
    };

    fetchData();
  }, [user]);

  // Map profiles for fast lookup
  const profileMap = useMemo(
    () =>
      profiles.reduce((acc, p) => {
        acc[p.id] = p.name;
        return acc;
      }, {}),
    [profiles]
  );

  // Form change handler
  const handleChange = (e, isNumber = false) => {
    const value = isNumber ? parseInt(e.target.value) : e.target.value;
    setFormData({ ...formData, [e.target.name]: value });
  };

  // Map form data to API payload
  const mapFormToAPI = (data) => ({
    employee_id: data.userId || null,
    rating: Number(data.score) || 0,
    remarks: data.remarks || "",
  });

  // Submit form
  const handleSubmit = async (e) => {
    e.preventDefault();
    const submitData = mapFormToAPI(formData);

    try {
      if (formData.id) {
        await updatePerformance(formData.id, submitData);
      } else {
        await addPerformance(submitData);
      }

      // Refresh performance list
      const updated = await getPerformance(user.profile);
      setPerformances(updated.data || updated);

      // Reset form
      setFormData({ userId: "", score: "", remarks: "" });
    } catch (err) {
      console.error("Error submitting performance:", err);
      alert("❌ Failed to save performance. Check console.");
    }
  };

  // Edit performance
  const handleEdit = (item) => setFormData(item);

  // Delete performance (optimistic update)
  const handleDelete = async (id) => {
    try {
      await deletePerformance(id);
      setPerformances((prev) => prev.filter((p) => p.id !== id));
    } catch (err) {
      console.error("Delete failed:", err);
      alert("❌ Failed to delete performance.");
    }
  };

  return (
    <Box className="performance-page">
      {/* ===== HERO HEADER ===== */}
      <section className="hero">
        <div className="hero-overlay">
          <h1>Performance Dashboard</h1>
          <p>Track and manage employee performance scores</p>
        </div>
      </section>

      {/* ===== MAIN CONTAINER ===== */}
      <Box className="dashboard-container">
        {/* --- FORM CARD --- */}
        <div className="dashboard-card">
          <Typography variant="h5" align="center" gutterBottom>
            {isAdmin ? "Add / Update Performance" : "My Performance"}
          </Typography>

          <form onSubmit={handleSubmit}>
            <FormControl fullWidth margin="normal">
              <InputLabel id="employee-label">Employee</InputLabel>
              <Select
                labelId="employee-label"
                name="userId"
                value={formData.userId || ""}
                onChange={(e) => handleChange(e, true)}
                disabled={!isAdmin}
                required
              >
                <MenuItem value="">Select Employee</MenuItem>
                {profiles.map((p) => (
                  <MenuItem key={p.id} value={p.id}>
                    {p.name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            <TextField
              label="Performance Score"
              name="score"
              type="number"
              fullWidth
              margin="normal"
              value={formData.score}
              onChange={handleChange}
              inputProps={{ min: 0, max: 100 }}
              required
            />

            <TextField
              label="Remarks"
              name="remarks"
              fullWidth
              margin="normal"
              value={formData.remarks}
              onChange={handleChange}
            />

            <Button type="submit" variant="contained" color="primary" fullWidth>
              {formData.id ? "Update" : "Add"}
            </Button>
          </form>
        </div>

        {/* --- CHARTS SECTION --- */}
        <div className="chart-section">
          <div className="chart-card">
            <Typography variant="h6" align="center">
              Performance Overview (Chart 1)
            </Typography>
            <p className="text-center mt-2">[Insert Pie or Bar Chart]</p>
          </div>

          <div className="chart-card">
            <Typography variant="h6" align="center">
              Score Distribution (Chart 2)
            </Typography>
            <p className="text-center mt-2">[Insert Radial or Line Chart]</p>
          </div>
        </div>

        {/* --- TABLE CARD --- */}
        <div className="dashboard-card table-wrapper">
          <h2>Performance Records</h2>
          <TableContainer component={Paper} className="modern-table">
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>ID</TableCell>
                  <TableCell>Employee</TableCell>
                  <TableCell>Score</TableCell>
                  <TableCell>Remarks</TableCell>
                  {isAdmin && <TableCell>Actions</TableCell>}
                </TableRow>
              </TableHead>
              <TableBody>
                {performances.map((perf) => (
                  <TableRow key={perf.id}>
                    <TableCell>{perf.id}</TableCell>
                    <TableCell>{profileMap[perf.userId] || "N/A"}</TableCell>
                    <TableCell>{perf.score}</TableCell>
                    <TableCell>{perf.remarks}</TableCell>
                    {isAdmin && (
                      <TableCell>
                        <Button
                          color="primary"
                          onClick={() => handleEdit(perf)}
                        >
                          Edit
                        </Button>
                        <Button
                          color="error"
                          onClick={() => handleDelete(perf.id)}
                        >
                          Delete
                        </Button>
                      </TableCell>
                    )}
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </div>
      </Box>
    </Box>
  );
};

export default Performance;
