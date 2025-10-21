/**
 * Firebase Authentication Module
 * Handles user authentication with Firebase (Email/Password and Google Sign-In)
 */

class FirebaseAuthManager {
    constructor() {
        this.auth = window.firebaseAuth;
        this.currentUser = null;
        this.initAuthStateListener();
    }

    /**
     * Initialize Firebase auth state listener
     */
    initAuthStateListener() {
        if (!this.auth) {
            console.error('Firebase Auth not initialized');
            return;
        }

        this.auth.onAuthStateChanged(async (user) => {
            this.currentUser = user;

            if (user) {
                console.log('User signed in:', user.email);
                // Get ID token and send to Django backend
                await this.authenticateWithDjango(user);
            } else {
                console.log('User signed out');
            }
        });
    }

    /**
     * Register new user with email and password
     * @param {string} email - User email
     * @param {string} password - User password
     * @param {string} displayName - User display name (optional)
     * @returns {Promise<object>} User credential
     */
    async registerWithEmail(email, password, displayName = null) {
        try {
            const userCredential = await this.auth.createUserWithEmailAndPassword(email, password);

            // Update profile with display name if provided
            if (displayName && userCredential.user) {
                await userCredential.user.updateProfile({
                    displayName: displayName
                });
            }

            console.log('User registered successfully:', userCredential.user.email);
            return userCredential;
        } catch (error) {
            console.error('Registration error:', error);
            throw this.handleAuthError(error);
        }
    }

    /**
     * Sign in existing user with email and password
     * @param {string} email - User email
     * @param {string} password - User password
     * @returns {Promise<object>} User credential
     */
    async signInWithEmail(email, password) {
        try {
            const userCredential = await this.auth.signInWithEmailAndPassword(email, password);
            console.log('User signed in successfully:', userCredential.user.email);
            return userCredential;
        } catch (error) {
            console.error('Sign in error:', error);
            throw this.handleAuthError(error);
        }
    }

    /**
     * Sign in with Google using popup
     * @returns {Promise<object>} User credential
     */
    async signInWithGoogle() {
        try {
            const provider = new firebase.auth.GoogleAuthProvider();
            // Add additional scopes if needed
            provider.addScope('profile');
            provider.addScope('email');

            const userCredential = await this.auth.signInWithPopup(provider);
            console.log('User signed in with Google:', userCredential.user.email);
            return userCredential;
        } catch (error) {
            console.error('Google sign in error:', error);
            throw this.handleAuthError(error);
        }
    }

    /**
     * Sign in with Google using redirect (better for mobile)
     * @returns {Promise<void>}
     */
    async signInWithGoogleRedirect() {
        try {
            const provider = new firebase.auth.GoogleAuthProvider();
            provider.addScope('profile');
            provider.addScope('email');

            await this.auth.signInWithRedirect(provider);
        } catch (error) {
            console.error('Google redirect sign in error:', error);
            throw this.handleAuthError(error);
        }
    }

    /**
     * Get redirect result after Google sign-in redirect
     * @returns {Promise<object>} User credential or null
     */
    async getRedirectResult() {
        try {
            const result = await this.auth.getRedirectResult();
            if (result.user) {
                console.log('User signed in via redirect:', result.user.email);
            }
            return result;
        } catch (error) {
            console.error('Redirect result error:', error);
            throw this.handleAuthError(error);
        }
    }

    /**
     * Sign out current user
     * @returns {Promise<void>}
     */
    async signOut() {
        try {
            await this.auth.signOut();
            // Also clear Django session
            await fetch('/api/auth/logout/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.getCsrfToken()
                }
            });
            console.log('User signed out successfully');
            window.location.href = '/';
        } catch (error) {
            console.error('Sign out error:', error);
            throw error;
        }
    }

    /**
     * Send password reset email
     * @param {string} email - User email
     * @returns {Promise<void>}
     */
    async resetPassword(email) {
        try {
            await this.auth.sendPasswordResetEmail(email);
            console.log('Password reset email sent to:', email);
        } catch (error) {
            console.error('Password reset error:', error);
            throw this.handleAuthError(error);
        }
    }

    /**
     * Get current user's ID token
     * @param {boolean} forceRefresh - Force refresh the token
     * @returns {Promise<string>} ID token
     */
    async getIdToken(forceRefresh = false) {
        if (!this.currentUser) {
            throw new Error('No user signed in');
        }

        try {
            const idToken = await this.currentUser.getIdToken(forceRefresh);
            return idToken;
        } catch (error) {
            console.error('Error getting ID token:', error);
            throw error;
        }
    }

    /**
     * Authenticate with Django backend using Firebase ID token
     * @param {object} user - Firebase user object
     * @returns {Promise<object>} Django response
     */
    async authenticateWithDjango(user) {
        try {
            const idToken = await user.getIdToken();

            const response = await fetch('/api/auth/firebase-login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCsrfToken()
                },
                body: JSON.stringify({
                    idToken: idToken
                })
            });

            const data = await response.json();

            if (response.ok) {
                console.log('Django authentication successful');
                return data;
            } else {
                console.error('Django authentication failed:', data.error);
                throw new Error(data.error || 'Authentication failed');
            }
        } catch (error) {
            console.error('Django authentication error:', error);
            throw error;
        }
    }

    /**
     * Get CSRF token from cookie
     * @returns {string} CSRF token
     */
    getCsrfToken() {
        const name = 'csrftoken';
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    /**
     * Handle Firebase auth errors and return user-friendly messages
     * @param {object} error - Firebase error object
     * @returns {Error} Formatted error
     */
    handleAuthError(error) {
        const errorMessages = {
            'auth/email-already-in-use': 'This email is already registered. Please sign in instead.',
            'auth/invalid-email': 'Please enter a valid email address.',
            'auth/operation-not-allowed': 'This sign-in method is not enabled.',
            'auth/weak-password': 'Password should be at least 6 characters.',
            'auth/user-disabled': 'This account has been disabled.',
            'auth/user-not-found': 'No account found with this email.',
            'auth/wrong-password': 'Incorrect password. Please try again.',
            'auth/too-many-requests': 'Too many failed attempts. Please try again later.',
            'auth/network-request-failed': 'Network error. Please check your connection.',
            'auth/popup-blocked': 'Popup was blocked by the browser. Please allow popups for this site.',
            'auth/popup-closed-by-user': 'Sign-in popup was closed before completion.',
            'auth/account-exists-with-different-credential': 'An account already exists with this email but different sign-in credentials.'
        };

        const message = errorMessages[error.code] || error.message || 'An error occurred during authentication.';
        return new Error(message);
    }

    /**
     * Check if user is currently signed in
     * @returns {boolean} True if user is signed in
     */
    isSignedIn() {
        return this.currentUser !== null;
    }

    /**
     * Get current user
     * @returns {object|null} Current Firebase user or null
     */
    getCurrentUser() {
        return this.currentUser;
    }
}

// Initialize Firebase Auth Manager when DOM is ready
let firebaseAuthManager;

document.addEventListener('DOMContentLoaded', function() {
    if (window.firebaseAuth) {
        firebaseAuthManager = new FirebaseAuthManager();
        window.firebaseAuthManager = firebaseAuthManager;
    } else {
        console.error('Firebase Auth not available. Please check Firebase configuration.');
    }
});
