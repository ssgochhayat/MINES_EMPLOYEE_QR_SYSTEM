import 'dart:convert';

import 'package:http/http.dart' as http;

import '../config/api.dart';

class ApiService {
  static String get baseUrl => ApiConfig.baseUrl;

  static Uri _uri(String path) => Uri.parse('$baseUrl$path');

  static Future<List<Map<String, dynamic>>> getEmployees() async {
    final response = await http.get(_uri('/employees/'));

    if (response.statusCode != 200) {
      throw Exception('Failed to load employees');
    }

    final decoded = jsonDecode(response.body);
    return List<Map<String, dynamic>>.from(decoded as List);
  }

  static Future<Map<String, dynamic>> getEmployeeByEmployeeId(
    String employeeId,
  ) async {
    final response = await http.get(_uri('/employees/$employeeId/'));

    if (response.statusCode != 200) {
      throw Exception('Employee not found');
    }

    return Map<String, dynamic>.from(jsonDecode(response.body) as Map);
  }

  static Future<Map<String, dynamic>?> resolveEmployeeFromQr(
    String rawCode,
  ) async {
    final code = rawCode.trim();
    if (code.isEmpty) return null;

    final employees = await getEmployees();
    final parsedUri = Uri.tryParse(code);
    final pathSegments = parsedUri?.pathSegments ?? const <String>[];

    String? pdfId;
    final pdfIndex = pathSegments.indexOf('employee-pdf');
    if (pdfIndex >= 0 && pathSegments.length > pdfIndex + 1) {
      pdfId = pathSegments[pdfIndex + 1];
    }

    String? employeeCode;
    final codeIndex = pathSegments.indexOf('code');
    if (codeIndex >= 0 && pathSegments.length > codeIndex + 1) {
      employeeCode = pathSegments[codeIndex + 1];
    }

    final candidates = <String>{
      code,
      if (pdfId != null) pdfId,
      if (employeeCode != null) employeeCode,
      if (pathSegments.isNotEmpty) pathSegments.last,
    };

    for (final employee in employees) {
      final id = _stringValue(employee['id']);
      final employeeId = _stringValue(employee['employee_id']);
      final pdfUrl = _stringValue(employee['employee_pdf']);

      if (candidates.contains(id) ||
          candidates.contains(employeeId) ||
          (pdfUrl.isNotEmpty && code.contains(pdfUrl))) {
        return employee;
      }
    }

    if (employeeCode != null && employeeCode.isNotEmpty) {
      try {
        return await getEmployeeByEmployeeId(employeeCode);
      } catch (_) {
        return null;
      }
    }

    return null;
  }

  static String _stringValue(dynamic value) {
    if (value == null) return '';
    return value.toString();
  }
}
