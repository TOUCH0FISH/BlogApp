import 'package:flutter/material.dart';
import 'dart:convert';
import 'login_page.dart';
import '../models/models.dart';
import '../models/user.dart';
import '../services/secure_storage_service.dart';
import '../services/auth_service.dart';
import '../services/user_service.dart';
import 'user_list_page.dart';
import 'blog_list_page.dart';

class HomePage extends StatefulWidget {
  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final AuthService _authService = AuthService();
  final UserService _userService = UserService();
  final SecureStorageService _secureStorageService = SecureStorageService();

  Widget _currentScreen = HomeScreen();
  bool _isLoggedIn = false;
  String _token = '';
  String _username = '';
  String _userRole = '';

  @override
  void initState() {
    super.initState();
    _checkLoginStatus();
  }

  void _checkLoginStatus() async {
    final token = await _secureStorageService.getToken();
    if (token != null && token.isNotEmpty) {
      try {
        final payload = json.decode(
          ascii.decode(
            base64.decode(
              base64.normalize(token.split(".")[1]),
            ),
          ),
        ) as Map<String, dynamic>;

        if (payload.containsKey('user_id') && payload['user_id'] != null) {
          final int userId = payload['user_id'];

          try {
            final User user = await _userService.getUser(userId);

            setState(() {
              _isLoggedIn = true;
              _token = token;
              _username = user.username;
              _userRole = user.role;
            });
          } catch (e) {
            print('Error fetching user by ID: $e');
          }
        } else {
          print('user_id not found in token');
        }
      } catch (e) {
        print('Error fetching user details: $e');
      }
    }
  }

  void _updateScreen(Widget screen) {
    setState(() {
      _currentScreen = screen;
    });
  }

  void _toggleLogin() async {
    // Open the login page as a dialog
    final result = await showDialog(
      context: context,
      builder: (BuildContext context) {
        return Dialog(
          child: LoginPage(),
        );
      },
    );

    if (result != null && result is AuthResponse) {
      setState(() {
        _isLoggedIn = true;
        _token = result.token ?? '';
        _username = result.user?.username ?? 'Guest';
        _userRole = result.user?.role ?? '-';
      });
    }
  }

  void _logout() async {
    try {
      final token = await _secureStorageService.getToken();
      if (token != null) {
        await _authService.logout(token);
        await _secureStorageService.deleteToken();
      }

      setState(() {
        _isLoggedIn = false;
        _username = '';
        _userRole = '';
        _token = '';
      });

      Navigator.of(context).pushReplacementNamed('/login');
    } catch (e) {
      print('Login error: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('BLOG'),
        actions: <Widget>[
          IconButton(
            icon: Icon(_isLoggedIn
                ? Icons.account_circle
                : Icons.account_circle_outlined),
            onPressed: () {
              // Add action for when the avatar icon is tapped
            },
          ),
        ],
      ),
      drawer: Drawer(
        child: ListView(
          padding: EdgeInsets.zero,
          children: <Widget>[
            DrawerHeader(
              decoration: BoxDecoration(
                color: Colors.purple,
              ),
              child: _isLoggedIn
                  ? Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      mainAxisAlignment: MainAxisAlignment.spaceAround,
                      children: <Widget>[
                        Text(
                          'Welcome, $_username',
                          style: TextStyle(
                            color: Colors.white,
                            fontSize: 20,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        Text(
                          'Role: $_userRole',
                          style: TextStyle(
                            color: Colors.white,
                            fontSize: 16,
                          ),
                        ),
                        ElevatedButton(
                          onPressed: _logout,
                          child: Text('Logout'),
                          style: ElevatedButton.styleFrom(
                            primary: Colors.red,
                            onPrimary: Colors.white,
                          ),
                        ),
                      ],
                    )
                  : Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: <Widget>[
                        Text(
                          'Please log in',
                          style: TextStyle(
                            color: Colors.white,
                            fontSize: 20,
                          ),
                        ),
                        SizedBox(height: 10),
                        ElevatedButton(
                          onPressed: _toggleLogin,
                          child: Text('Login'),
                        ),
                      ],
                    ),
            ),
            ListTile(
              title: Text('Home'),
              onTap: () {
                _updateScreen(HomeScreen());
              },
            ),
            ListTile(
              title: Text('Posts'),
              onTap: () {
                _updateScreen(BlogListPage());
              },
            ),
            ListTile(
              title: Text('Users'),
              onTap: () {
                _updateScreen(UserListPage());
              },
            ),
            // Add other menu items here
          ],
        ),
      ),
      body: _currentScreen,
    );
  }
}

// Placeholder widget for HomeScreen
class HomeScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Center(
      child: Text('Home Screen'),
    );
  }
}

// // Placeholder widget for MaterialsScreen
// class MaterialsScreen extends StatelessWidget {
//   @override
//   Widget build(BuildContext context) {
//     return Center(
//       child: Text('Materials Screen'),
//     );
//   }
// }
