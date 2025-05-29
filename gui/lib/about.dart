import 'package:flutter/material.dart';
import 'package:package_info_plus/package_info_plus.dart';
import 'package:url_launcher/url_launcher.dart';

class WebPage {
  final String url;
  WebPage.issues()
      : url = 'https://github.com/JasperVanDenBosch/latency-recorder/issues';
}

class AboutSection extends StatefulWidget {
  const AboutSection({super.key});

  @override
  State<AboutSection> createState() => _AboutSectionState();
}

class _AboutSectionState extends State<AboutSection> {
  String version = '0.0.0';

  @override
  void initState() {
    super.initState();
    PackageInfo.fromPlatform().then((PackageInfo packageInfo) {
      setState(() {
        version = packageInfo.version;
      });
    });
  }

  void openWebPage(WebPage page) {
    final Uri uri = Uri.parse(page.url);
    launchUrl(uri);
  }

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.end,
      children: [
        Text(version),
        const SizedBox(width: 10),
        IconButton(
          onPressed: () {
            openWebPage(WebPage.issues());
          },
          tooltip: 'Report Issue',
          icon: const Icon(Icons.bug_report)
        )
      ],
    );
  }
}