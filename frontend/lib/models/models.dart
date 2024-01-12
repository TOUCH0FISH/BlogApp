import 'user.dart';

class AuthResponse {
  final String? token;
  final User? user;
  final String? message;

  AuthResponse({this.token, this.user, this.message});

  factory AuthResponse.fromJson(Map<String, dynamic> json) {
    return AuthResponse(
      token: json['token'],
      user: json.containsKey('user') ? User.fromJson(json['user']) : null,
      message: json['message'],
    );
  }
}
