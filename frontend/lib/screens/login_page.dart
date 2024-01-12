import 'package:citobe/screens/register_page.dart';
import 'package:flutter/material.dart';
import '../services/auth_service.dart';
import '../services/secure_storage_service.dart';
import '../models/models.dart';

class LoginPage extends StatefulWidget {
  @override
  _LoginPageState createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final _formKey = GlobalKey<FormState>();
  final AuthService _authService = AuthService();
  final FocusNode _loginFocusNode = FocusNode();

  AuthResponse? response;

  bool _isLoading = false;

  String _username = '';
  String _password = '';

  @override
  void dispose() {
    _loginFocusNode.dispose();
    super.dispose();
  }

  void _submit() async {
    if (_formKey.currentState!.validate()) {
      _formKey.currentState!.save();

      try {
        final response = await _authService.login(_username, _password);
        if (response.token != null) {
          await SecureStorageService().saveToken(response.token!);
          setState(() {
            _isLoading = true;
          });
          Navigator.of(context).popAndPushNamed('/home');
          print('Login successful: $response');
        }
      } catch (e) {
        Navigator.of(context).pop(response);
        print('Login error: $e');
      } finally {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Login')),
      body: Padding(
        padding: EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: Column(
            children: <Widget>[
              TextFormField(
                focusNode: _loginFocusNode,
                autofocus: true,
                decoration: InputDecoration(labelText: 'Username'),
                validator: (value) =>
                    value!.isEmpty ? 'Please enter username' : null,
                onSaved: (value) => _username = value!,
              ),
              TextFormField(
                decoration: InputDecoration(labelText: 'Password'),
                obscureText: true,
                validator: (value) =>
                    value!.isEmpty ? 'Please enter password' : null,
                onSaved: (value) => _password = value!,
              ),
              ElevatedButton(
                onPressed: _submit,
                child: Text('Login'),
              ),
              ElevatedButton(
                onPressed: () {
                  onGenerateRoute:
                  (settings) {
                    if (settings.name == '/register') {
                      return MaterialPageRoute(
                          builder: (context) => RegisterPage());
                    }
                    // 处理其他路由...
                  };
                  Navigator.pushNamed(context, '/register');
                },
                child: Text('Register'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
