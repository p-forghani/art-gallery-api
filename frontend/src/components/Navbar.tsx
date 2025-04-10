import React from 'react';
import { AppBar, Toolbar, Button, Typography, Box, Container } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Navbar: React.FC = () => {
  const { isAuthenticated, user, logout } = useAuth();

  return (
    <AppBar position="sticky" elevation={1} sx={{ backgroundColor: 'white', color: 'primary.main' }}>
      <Container maxWidth="lg">
        <Toolbar disableGutters>
          <Typography
            variant="h4"
            component={RouterLink}
            to="/"
            sx={{
              flexGrow: 1,
              fontWeight: 700,
              textDecoration: 'none',
              color: 'primary.main',
              '&:hover': {
                color: 'primary.dark',
              },
            }}
          >
            Negar Studio
          </Typography>
          <Box sx={{ display: 'flex', gap: 2 }}>
            <Button
              component={RouterLink}
              to="/"
              sx={{
                color: 'primary.main',
                '&:hover': {
                  backgroundColor: 'primary.light',
                  color: 'white',
                },
              }}
            >
              Gallery
            </Button>
            {isAuthenticated ? (
              <>
                <Button
                  component={RouterLink}
                  to="/admin"
                  sx={{
                    color: 'primary.main',
                    '&:hover': {
                      backgroundColor: 'primary.light',
                      color: 'white',
                    },
                  }}
                >
                  Admin
                </Button>
                <Button
                  onClick={logout}
                  sx={{
                    color: 'secondary.main',
                    '&:hover': {
                      backgroundColor: 'secondary.light',
                      color: 'white',
                    },
                  }}
                >
                  Logout ({user})
                </Button>
              </>
            ) : (
              <>
                <Button
                  component={RouterLink}
                  to="/login"
                  sx={{
                    color: 'primary.main',
                    '&:hover': {
                      backgroundColor: 'primary.light',
                      color: 'white',
                    },
                  }}
                >
                  Login
                </Button>
                <Button
                  component={RouterLink}
                  to="/register"
                  variant="contained"
                  color="secondary"
                  sx={{
                    '&:hover': {
                      backgroundColor: 'secondary.dark',
                    },
                  }}
                >
                  Register
                </Button>
              </>
            )}
          </Box>
        </Toolbar>
      </Container>
    </AppBar>
  );
};

export default Navbar; 