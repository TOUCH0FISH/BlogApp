import 'package:flutter/material.dart';
import 'services/secure_storage_service.dart';
import 'screens/login_page.dart';
import 'screens/home_page.dart';
import 'screens/register_page.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  final SecureStorageService _secureStorageService = SecureStorageService();

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Blog',
      initialRoute: '/',
      routes: {
        '/login': (context) => LoginPage(),
        '/home': (context) => HomePage(),
        
        '/register': (context) => RegisterPage(),
        // Add other routes here
      },
      home: FutureBuilder<String?>(
        future: _secureStorageService.getToken(),
        builder: (BuildContext context, AsyncSnapshot<String?> snapshot) {
          if (snapshot.connectionState == ConnectionState.done) {
            if (snapshot.data != null && snapshot.data!.isNotEmpty) {
              return HomePage(); // User is already logged in
            } else {
              return LoginPage(); // User needs to log in
            }
          }
          return CircularProgressIndicator(); // Show loading indicator while checking token
        },
      ),
    );
  }
}
