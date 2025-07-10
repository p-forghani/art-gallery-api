import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate, useNavigate, useParams } from 'react-router-dom';
import { AuthProvider, useAuth } from './AuthContext';
import StorePage from './StorePage';
import ArtistPage from './ArtistPage';
import ProfilePage from './ProfilePage';
import { getArtworks, getArtwork, getArtistDashboard } from './api';
import { AppBar, Toolbar, Button, Container, Typography, CircularProgress, List, ListItem, ListItemText, Box, Paper, TextField, Alert } from '@mui/material';

function RequireAuth({ children }) {
  const { user, loading } = useAuth();
  if (loading) return null;
  if (!user) return <Navigate to="/login" replace />;
  return children;
}

function NavBar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  return (
    <AppBar position="static">
      <Toolbar>
        <Button color="inherit" component={Link} to="/">Store</Button>
        {user && user.role_id === 2 && (
          <Button color="inherit" component={Link} to="/artist">Artist</Button>
        )}
        {user && (
          <Button color="inherit" component={Link} to="/profile">Profile</Button>
        )}
        <Box sx={{ flexGrow: 1 }} />
        {user ? (
          <>
            <Typography variant="body1" sx={{ mr: 2 }}>{user.name}</Typography>
            <Button color="inherit" onClick={() => { logout(); navigate('/'); }}>Logout</Button>
          </>
        ) : (
          <>
            <Button color="inherit" component={Link} to="/login">Login</Button>
            <Button color="inherit" component={Link} to="/register">Register</Button>
          </>
        )}
      </Toolbar>
    </AppBar>
  );
}

function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = React.useState({ email: '', password: '' });
  const [error, setError] = React.useState(null);
  const handleChange = e => setForm(f => ({ ...f, [e.target.name]: e.target.value }));
  const handleSubmit = async e => {
    e.preventDefault();
    setError(null);
    try {
      await login(form);
      navigate('/');
    } catch (err) {
      setError('Invalid credentials');
    }
  };
  return (
    <Container maxWidth="xs">
      <Box sx={{ mt: 8 }}>
        <Typography variant="h5" align="center">Login</Typography>
        {error && <Alert severity="error">{error}</Alert>}
        <form onSubmit={handleSubmit}>
          <TextField label="Email" name="email" fullWidth margin="normal" value={form.email} onChange={handleChange} required />
          <TextField label="Password" name="password" type="password" fullWidth margin="normal" value={form.password} onChange={handleChange} required />
          <Button type="submit" variant="contained" color="primary" fullWidth sx={{ mt: 2 }}>Login</Button>
        </form>
      </Box>
    </Container>
  );
}

function RegisterPage() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = React.useState({ name: '', email: '', password: '' });
  const [error, setError] = React.useState(null);
  const handleChange = e => setForm(f => ({ ...f, [e.target.name]: e.target.value }));
  const handleSubmit = async e => {
    e.preventDefault();
    setError(null);
    try {
      await register(form);
      navigate('/');
    } catch (err) {
      setError('Registration failed');
    }
  };
  return (
    <Container maxWidth="xs">
      <Box sx={{ mt: 8 }}>
        <Typography variant="h5" align="center">Register</Typography>
        {error && <Alert severity="error">{error}</Alert>}
        <form onSubmit={handleSubmit}>
          <TextField label="Name" name="name" fullWidth margin="normal" value={form.name} onChange={handleChange} required />
          <TextField label="Email" name="email" fullWidth margin="normal" value={form.email} onChange={handleChange} required />
          <TextField label="Password" name="password" type="password" fullWidth margin="normal" value={form.password} onChange={handleChange} required />
          <Button type="submit" variant="contained" color="primary" fullWidth sx={{ mt: 2 }}>Register</Button>
        </form>
      </Box>
    </Container>
  );
}

function ArtworkDetailPage() {
  const { id } = useParams();
  const [artwork, setArtwork] = React.useState(null);
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState(null);
  React.useEffect(() => {
    getArtwork(id).then(res => setArtwork(res.data)).catch(() => setError('Failed to load artwork')).finally(() => setLoading(false));
  }, [id]);
  if (loading) return <CircularProgress />;
  if (error) return <Alert severity="error">{error}</Alert>;
  if (!artwork) return <Typography>No artwork found.</Typography>;
  return (
    <Container maxWidth="sm" sx={{ mt: 4 }}>
      <Paper sx={{ p: 2 }}>
        <Typography variant="h5">{artwork.title}</Typography>
        <Typography variant="body1">{artwork.description}</Typography>
        {artwork.image_url && <img src={artwork.image_url} alt={artwork.title} style={{ width: '100%', marginTop: 16 }} />}
      </Paper>
    </Container>
  );
}

function ArtistDashboardPage() {
  const [artworks, setArtworks] = React.useState([]);
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState(null);
  React.useEffect(() => {
    getArtistDashboard().then(setArtworks).catch(() => setError('Failed to load dashboard')).finally(() => setLoading(false));
  }, []);
  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom>Artist Dashboard</Typography>
      {loading && <CircularProgress />}
      {error && <Alert severity="error">{error}</Alert>}
      <List>
        {artworks.map(art => (
          <ListItem key={art.id} divider>
            <ListItemText primary={art.title} secondary={art.description} />
          </ListItem>
        ))}
      </List>
    </Container>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <Router>
        <NavBar />
        <Routes>
          <Route path="/" element={<StorePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/profile" element={<RequireAuth><ProfilePage /></RequireAuth>} />
          <Route path="/artist" element={<RequireAuth><ArtistPage /></RequireAuth>} />
          <Route path="/artwork/:id" element={<ArtworkDetailPage />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}
