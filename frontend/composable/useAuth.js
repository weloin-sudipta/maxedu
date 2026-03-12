export const logout = async () => {
    try {
        const response = await fetch('/api/method/logout', {
            method: 'GET',
            credentials: 'same-origin',
        });

        if (response.ok) {
            window.location.href = '/auth/login';
        } else {
            const data = await response.json();
            throw new Error(data.message || 'Logout failed');
        }
    } catch (error) {
        console.error('Error during logout:', error);
        throw error;
    }
};

export const login = async (usr, pwd) => {
    try {
        const response = await fetch('/api/method/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({
                usr: usr,
                pwd: pwd
            })
        });

        const data = await response.json();

        if (response.ok) {
            window.location.href = '/';
            console.log('Logged in successfully:', data);
        } else {
            throw new Error(data.message || 'Login failed');
        }

    } catch (error) {
        console.error('Error during login:', error);
        throw error;
    }
};