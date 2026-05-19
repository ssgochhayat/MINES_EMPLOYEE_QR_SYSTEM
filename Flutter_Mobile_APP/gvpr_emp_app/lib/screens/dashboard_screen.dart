import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../widgets/dashboard_card.dart';
import 'employee_screen.dart';
import 'qr_scanner_screen.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  List employees = [];

  bool loading = true;

  @override
  void initState() {
    super.initState();
    loadEmployees();
  }

  Future<void> loadEmployees() async {
    try {
      final data = await ApiService.getEmployees();

      setState(() {
        employees = data;
        loading = false;
      });
    } catch (e) {
      setState(() {
        loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey.shade100,
      appBar: AppBar(
        elevation: 0,
        backgroundColor: Colors.white,
        title: const Text(
          "GVPR Employee Dashboard",
          style: TextStyle(
            color: Colors.black,
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
      body: loading
          ? const Center(
              child: CircularProgressIndicator(),
            )
          : SingleChildScrollView(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    "Welcome Admin 👋",
                    style: TextStyle(
                      fontSize: 28,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 20),
                  GridView.count(
                    crossAxisCount: 2,
                    shrinkWrap: true,
                    physics: const NeverScrollableScrollPhysics(),
                    crossAxisSpacing: 15,
                    mainAxisSpacing: 15,
                    childAspectRatio: 1.5,
                    children: [
                      /// Total Employees
                      DashboardCard(
                        title: "Total Employees",
                        value: employees.length.toString(),
                        icon: Icons.people,
                        color: Colors.blue,
                      ),

                      /// Departments
                      DashboardCard(
                        title: "Departments",
                        value: employees
                            .map((e) => e['department'])
                            .toSet()
                            .length
                            .toString(),
                        icon: Icons.apartment,
                        color: Colors.orange,
                      ),

                      /// QR Scans
                      DashboardCard(
                        title: "QR Scans",
                        value: employees.length.toString(),
                        icon: Icons.qr_code_scanner,
                        color: Colors.green,
                      ),

                      /// Documents
                      DashboardCard(
                        title: "Documents",
                        value: employees
                            .fold(
                              0,
                              (sum, e) =>
                                  sum +
                                  ((e['documents'] as List?)?.length ?? 0),
                            )
                            .toString(),
                        icon: Icons.picture_as_pdf,
                        color: Colors.red,
                      ),
                    ],
                  ),
                  const SizedBox(height: 30),
                  const Text(
                    "Quick Actions",
                    style: TextStyle(
                      fontSize: 22,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 20),
                  Row(
                    children: [
                      /// Employee Button
                      Expanded(
                        child: ElevatedButton.icon(
                          style: ElevatedButton.styleFrom(
                            padding: const EdgeInsets.all(18),
                            backgroundColor: Colors.blue,
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(18),
                            ),
                          ),
                          onPressed: () {
                            Navigator.push(
                              context,
                              MaterialPageRoute(
                                builder: (_) => const EmployeeScreen(),
                              ),
                            );
                          },
                          icon: const Icon(
                            Icons.people,
                            color: Colors.white,
                          ),
                          label: const Text(
                            "Employees",
                            style: TextStyle(
                              color: Colors.white,
                            ),
                          ),
                        ),
                      ),

                      const SizedBox(width: 15),

                      /// QR Scanner Button
                      Expanded(
                        child: ElevatedButton.icon(
                          style: ElevatedButton.styleFrom(
                            padding: const EdgeInsets.all(18),
                            backgroundColor: Colors.green,
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(18),
                            ),
                          ),
                          onPressed: () {
                            Navigator.push(
                              context,
                              MaterialPageRoute(
                                builder: (_) => const QRScannerScreen(),
                              ),
                            );
                          },
                          icon: const Icon(
                            Icons.qr_code_scanner,
                            color: Colors.white,
                          ),
                          label: const Text(
                            "Scan QR",
                            style: TextStyle(
                              color: Colors.white,
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 30),
                  const Text(
                    "Recent Employees",
                    style: TextStyle(
                      fontSize: 22,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 15),
                  ListView.builder(
                    shrinkWrap: true,
                    physics: const NeverScrollableScrollPhysics(),
                    itemCount: employees.length,
                    itemBuilder: (context, index) {
                      final emp = employees[index];

                      return Card(
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(18),
                        ),
                        child: ListTile(
                          leading: CircleAvatar(
                            backgroundImage:
                                emp['photo'] != null && emp['photo'] != ''
                                    ? NetworkImage(emp['photo'])
                                    : null,
                            child: emp['photo'] == ''
                                ? const Icon(Icons.person)
                                : null,
                          ),
                          title: Text(
                            emp['name'],
                          ),
                          subtitle: Text(
                            emp['designation'],
                          ),
                          trailing: const Icon(
                            Icons.arrow_forward_ios,
                          ),
                          onTap: () {},
                        ),
                      );
                    },
                  ),
                ],
              ),
            ),
    );
  }
}
