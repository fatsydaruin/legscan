import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:intl/intl.dart';
import '../models/mover.dart';

class SupabaseService {
  static final SupabaseClient _client = Supabase.instance.client;

  /// Fetches gainers or losers for a specific date.
  static Future<List<Mover>> getMovers({
    required DateTime date,
    required String category, // 'gainer' or 'loser'
  }) async {
    final dateStr = DateFormat('yyyy-MM-dd').format(date);

    final response = await _client
        .from('daily_movers')
        .select()
        .eq('trade_date', dateStr)
        .eq('category', category)
        .order('pct_change', ascending: category == 'loser');
    // gainers: highest first (descending, default from query since we override below)
    // losers: most negative first (ascending)

    final data = response as List<dynamic>;
    return data.map((row) => Mover.fromJson(row as Map<String, dynamic>)).toList();
  }

  /// Returns list of distinct dates that have data (for enabling date picker days)
  static Future<Set<DateTime>> getAvailableDates() async {
    final response = await _client
        .from('daily_movers')
        .select('trade_date')
        .order('trade_date', ascending: false);

    final data = response as List<dynamic>;
    final dates = data
        .map((row) => DateTime.parse(row['trade_date'] as String))
        .toSet();
    return dates;
  }
}
