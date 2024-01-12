import 'package:flutter/material.dart';
import '../models/user.dart';
import '../services/user_service.dart';

class UserForm extends StatefulWidget {
  // Pass null for creating a new user, pass a User object for editing
  final User? user;
  final VoidCallback onUserUpdated;

  UserForm({this.user, required this.onUserUpdated});

  @override
  _UserFormState createState() => _UserFormState();
}

class _UserFormState extends State<UserForm> {
  final UserService _userService = UserService();
  final _formKey = GlobalKey<FormState>();
  final FocusNode _usernameFocusNode = FocusNode();
  String _username = '';
  String _role = '';

  @override
  void initState() {
    super.initState();
    if (widget.user != null) {
      _username = widget.user!.username;
      _role = widget.user!.role;
    }
  }

  @override
  void dispose() {
    _usernameFocusNode.dispose();
    super.dispose();
  }

  void _submit() async {
    if (_formKey.currentState!.validate()) {
      _formKey.currentState!.save();

      try {
        User user;
        if (widget.user == null) {
          user = User(
            username: _username,
            role: _role,
            password: 'blog', // Default password for new users
          );
          await _userService.createUser(user);
          print('User created successfully');
        } else {
          user = User(
            userId: widget.user!.userId,
            username: _username,
            role: _role,
            // No password field here
          );
          await _userService.updateUser(user);
          print('User updated successfully');
        }

        widget.onUserUpdated();
        Navigator.pop(context); // Close the modal after submitting
      } catch (e) {
        print('Error: $e');
        // Show an error message to the user
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(12.0),
      child: Form(
        key: _formKey,
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: <Widget>[
            TextFormField(
              focusNode: _usernameFocusNode,
              autofocus: true,
              initialValue: _username,
              decoration: InputDecoration(labelText: 'Username'),
              onSaved: (value) => _username = value!,
              validator: (value) =>
                  value!.isEmpty ? 'Please enter username' : null,
            ),
            TextFormField(
              initialValue: _role,
              decoration: InputDecoration(labelText: 'Role'),
              onSaved: (value) => _role = value!,
              validator: (value) => value!.isEmpty ? 'Please enter role' : null,
            ),
            ElevatedButton(
              onPressed: _submit,
              child: Text(widget.user == null ? 'Create' : 'Update'),
            ),
          ],
        ),
      ),
    );
  }
}
