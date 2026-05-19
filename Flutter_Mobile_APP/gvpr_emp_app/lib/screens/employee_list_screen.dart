import 'package:flutter/material.dart';

import '../services/api_service.dart';
import 'employee_detail_screen.dart';

class EmployeeListScreen extends StatefulWidget {
  const EmployeeListScreen({super.key});

  @override
  State<EmployeeListScreen> createState() => _EmployeeListScreenState();
}

class _EmployeeListScreenState extends State<EmployeeListScreen> {
  List employees = [];

  @override
  void initState() {
    super.initState();
    loadEmployees();
  }

  void loadEmployees() async {
    final data = await ApiService.getEmployees();

    setState(() {
      employees = data;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Employees"),
      ),
      body: ListView.builder(
        itemCount: employees.length,
        itemBuilder: (context, index) {
          final emp = employees[index];

          return Card(
            margin: const EdgeInsets.all(10),
            child: ListTile(
              leading: CircleAvatar(
                backgroundImage: emp['photo'] != null && emp['photo'] != ''
                    ? NetworkImage(emp['photo'])
                    : null,
                child: emp['photo'] == null || emp['photo'] == ''
                    ? const Icon(Icons.person)
                    : null,
              ),
              title: Text(emp['name']),
              subtitle: Text(
                "${emp['designation']} - ${emp['department']}",
              ),
              trailing: const Icon(Icons.arrow_forward),
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) => EmployeeDetailScreen(
                      employee: emp,
                    ),
                  ),
                );
              },
            ),
          );
        },
      ),
    );
  }
}
