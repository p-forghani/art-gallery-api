import React from 'react';
import { useAuth } from './AuthContext';
import { Container, Typography, Paper, Box } from '@mui/material';

export default function ProfilePage() {
  const { user } = useAuth();
  if (!user) return null;
  return (
    <Container maxWidth="sm" sx={{ mt: 4 }}>
      <Paper sx={{ p: 3 }}>
        <Typography variant="h5" gutterBottom>Profile</Typography>
        <Box>
          <Typography><b>Name:</b> {user.name}</Typography>
          <Typography><b>Email:</b> {user.email}</Typography>
          <Typography><b>Role ID:</b> {user.role_id}</Typography>
        </Box>
      </Paper>
    </Container>
  );
} 