import 'package:flutter/material.dart';
import '../models/user.dart';
import '../services/user_service.dart';
import '../widgets/user_form.dart';

class UserListPage extends StatefulWidget {
  @override
  _UserListPageState createState() => _UserListPageState();
}

class _UserListPageState extends State<UserListPage> {
  final UserService _userService = UserService();
  late List<User> _users = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadUsers();
  }

  Future<void> _loadUsers() async {
    try {
      _users = await _userService.getUsers();
    } catch (e) {
      print('Error loading users: $e');
    } finally {
      setState(() => _isLoading = false);
    }
  }

  Future<bool> _showDeleteConfirmation(BuildContext context) async {
    return await showDialog<bool>(
          context: context,
          builder: (BuildContext context) {
            return AlertDialog(
              title: Text("Confirm Deletion"),
              content: Text("Are you sure you want to delete this user?"),
              actions: <Widget>[
                TextButton(
                  child: Text("Cancel"),
                  onPressed: () => Navigator.of(context).pop(false),
                ),
                TextButton(
                  child: Text("Delete"),
                  onPressed: () => Navigator.of(context).pop(true),
                ),
              ],
            );
          },
        ) ??
        false;
  }

  void _onUserUpdated() {
    _loadUsers();
  }

  void _showUserForm(User? user) {
    showModalBottomSheet(
      context: context,
      builder: (context) => UserForm(user: user, onUserUpdated: _onUserUpdated),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Users')),
      body: _isLoading
          ? Center(child: CircularProgressIndicator())
          : ListView.builder(
              itemCount: _users.length,
              itemBuilder: (context, index) => _buildUserItem(_users[index]),
            ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          // Navigate to user creation form
          _showUserForm(null);
        },
        child: Icon(Icons.add),
      ),
    );
  }

  Widget _buildUserItem(User user) {
    return ListTile(
      title: Text(user.username),
      subtitle: Text(user.role),
      trailing: Row(
        mainAxisSize: MainAxisSize.min,
        children: <Widget>[
          IconButton(
            icon: Icon(Icons.edit),
            onPressed: () {
              // Navigate to edit user form
              _showUserForm(user);
            },
          ),
          IconButton(
            icon: Icon(Icons.delete),
            onPressed: () async {
              if (user.userId != null) {
                final confirm = await _showDeleteConfirmation(context);
                if (confirm) {
                  try {
                    await _userService.deleteUser(user.userId!);
                    _loadUsers();
                  } catch (e) {
                    // Handle or show an error message
                    print('Error deleting user: $e');
                  }
                }
              } else {
                // Handle the case where userId is null
                print('Cannot delete user with null ID');
              }
            },
          ),
        ],
      ),
    );
  }
}
