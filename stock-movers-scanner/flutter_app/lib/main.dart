import 'package:flutter/material.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'screens/movers_screen.dart';

// TODO: replace with your Supabase project credentials
const supabaseUrl = 'https://your-project-ref.supabase.co';
const supabaseAnonKey = 'your-anon-key';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Supabase.initialize(
    url: supabaseUrl,
    anonKey: supabaseAnonKey,
  );
  runApp(const StockMoversApp());
}

class StockMoversApp extends StatelessWidget {
  const StockMoversApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'NIFTY 500 Movers',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.indigo),
        useMaterial3: true,
      ),
      home: const MoversScreen(),
    );
  }
}
