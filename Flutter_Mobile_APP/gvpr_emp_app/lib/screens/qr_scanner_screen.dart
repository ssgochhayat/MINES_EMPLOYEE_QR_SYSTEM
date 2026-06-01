import 'package:flutter/material.dart';
import 'package:mobile_scanner/mobile_scanner.dart';
import 'package:url_launcher/url_launcher.dart';

class QRScannerScreen extends StatefulWidget {
  const QRScannerScreen({super.key});

  @override
  State<QRScannerScreen> createState() => _QRScannerScreenState();
}

class _QRScannerScreenState extends State<QRScannerScreen>
    with SingleTickerProviderStateMixin {
  final MobileScannerController controller = MobileScannerController();

  bool scanned = false;

  late AnimationController animationController;
  late Animation<double> animation;

  @override
  void initState() {
    super.initState();

    animationController = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 2),
    )..repeat(reverse: true);

    animation = Tween<double>(
      begin: -120,
      end: 120,
    ).animate(animationController);
  }

  @override
  void dispose() {
    animationController.dispose();
    controller.dispose();
    super.dispose();
  }

  void onDetect(BarcodeCapture capture) {
    if (scanned) return;

    final List<Barcode> barcodes = capture.barcodes;

    for (final barcode in barcodes) {
      final String code = barcode.rawValue ?? "";

      if (code.isNotEmpty) {
        scanned = true;

        showDialog(
          context: context,
          barrierDismissible: false,
          builder: (_) => AlertDialog(
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(20),
            ),
            title: const Row(
              children: [
                Icon(
                  Icons.check_circle,
                  color: Colors.green,
                ),
                SizedBox(width: 8),
                Text("QR Scan Successful"),
              ],
            ),
            content: SingleChildScrollView(
              child: Text(
                code,
                style: const TextStyle(
                  fontSize: 14,
                ),
              ),
            ),
            actions: [
              TextButton(
                onPressed: () {
                  Navigator.pop(context);

                  Future.delayed(
                    const Duration(seconds: 2),
                    () {
                      scanned = false;
                    },
                  );
                },
                child: const Text("Cancel"),
              ),
              ElevatedButton(
                onPressed: () async {
                  Navigator.pop(context);

                  try {
                    final Uri uri = Uri.parse(code);

                    print("Opening URL: $uri");

                    final bool launched = await launchUrl(
                      uri,
                      mode: LaunchMode.externalApplication,
                    );

                    if (!launched && mounted) {
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(
                          content: Text("Failed to open URL"),
                        ),
                      );
                    }
                  } catch (e) {
                    if (mounted) {
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(
                          content: Text("Error: $e"),
                        ),
                      );
                    }
                  }

                  Future.delayed(
                    const Duration(seconds: 2),
                    () {
                      scanned = false;
                    },
                  );
                },
                child: const Text("Open"),
              ),
            ],
          ),
        );

        break;
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xff0F172A),
      body: Stack(
        children: [
          /// CAMERA
          MobileScanner(
            controller: controller,
            onDetect: onDetect,
          ),

          /// DARK OVERLAY
          Container(
            color: Colors.black.withOpacity(0.45),
          ),

          /// TOP BAR
          SafeArea(
            child: Padding(
              padding: const EdgeInsets.symmetric(
                horizontal: 20,
                vertical: 15,
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text(
                    "Scan Employee QR",
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  Container(
                    decoration: BoxDecoration(
                      color: Colors.white.withOpacity(0.15),
                      borderRadius: BorderRadius.circular(15),
                    ),
                    child: IconButton(
                      onPressed: () {
                        controller.toggleTorch();
                      },
                      icon: const Icon(
                        Icons.flash_on,
                        color: Colors.white,
                      ),
                    ),
                  )
                ],
              ),
            ),
          ),

          /// SCANNER BOX
          Center(
            child: Container(
              width: 260,
              height: 260,
              decoration: BoxDecoration(
                border: Border.all(
                  color: Colors.greenAccent,
                  width: 3,
                ),
                borderRadius: BorderRadius.circular(25),
              ),
              child: Stack(
                children: [
                  AnimatedBuilder(
                    animation: animation,
                    builder: (context, child) {
                      return Positioned(
                        top: 130 + animation.value,
                        left: 0,
                        right: 0,
                        child: Container(
                          height: 3,
                          color: Colors.greenAccent,
                        ),
                      );
                    },
                  ),
                ],
              ),
            ),
          ),

          /// BOTTOM INFO
          Positioned(
            bottom: 40,
            left: 20,
            right: 20,
            child: Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: Colors.white.withOpacity(0.12),
                borderRadius: BorderRadius.circular(25),
                border: Border.all(
                  color: Colors.white24,
                ),
              ),
              child: const Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Icon(
                    Icons.qr_code_scanner,
                    color: Colors.greenAccent,
                    size: 40,
                  ),
                  SizedBox(height: 10),
                  Text(
                    "Place the employee QR code inside the frame",
                    textAlign: TextAlign.center,
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 16,
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
