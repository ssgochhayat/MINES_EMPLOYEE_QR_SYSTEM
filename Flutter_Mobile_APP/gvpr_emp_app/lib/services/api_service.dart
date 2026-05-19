import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  static const String baseUrl = "http://10.36.83.65:8000/api";

  static Future<List<dynamic>> getEmployees() async {
    final response = await http.get(Uri.parse("$baseUrl/employees/"));

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception("Failed to load employees");
    }
  }
}
