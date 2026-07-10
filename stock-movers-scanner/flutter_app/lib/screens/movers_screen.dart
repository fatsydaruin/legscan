import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../models/mover.dart';
import '../services/supabase_service.dart';
import '../widgets/mover_tile.dart';

class MoversScreen extends StatefulWidget {
  const MoversScreen({super.key});

  @override
  State<MoversScreen> createState() => _MoversScreenState();
}

class _MoversScreenState extends State<MoversScreen>
    with SingleTickerProviderStateMixin {
  late TabController _tabController;
  DateTime _selectedDate = DateTime.now();

  List<Mover> _gainers = [];
  List<Mover> _losers = [];
  bool _loading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 2, vsync: this);
    _loadData();
  }

  Future<void> _loadData() async {
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      final gainers = await SupabaseService.getMovers(
        date: _selectedDate,
        category: 'gainer',
      );
      final losers = await SupabaseService.getMovers(
        date: _selectedDate,
        category: 'loser',
      );
      setState(() {
        _gainers = gainers;
        _losers = losers;
        _loading = false;
      });
    } catch (e) {
      setState(() {
        _error = e.toString();
        _loading = false;
      });
    }
  }

  Future<void> _pickDate() async {
    final now = DateTime.now();
    final picked = await showDatePicker(
      context: context,
      initialDate: _selectedDate,
      firstDate: now.subtract(const Duration(days: 60)),
      lastDate: now,
    );
    if (picked != null) {
      setState(() => _selectedDate = picked);
      _loadData();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('NIFTY 500 Movers'),
        bottom: TabBar(
          controller: _tabController,
          tabs: [
            Tab(text: 'Gainers (${_gainers.length})'),
            Tab(text: 'Losers (${_losers.length})'),
          ],
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.calendar_today),
            onPressed: _pickDate,
          ),
        ],
      ),
      body: Column(
        children: [
          Container(
            width: double.infinity,
            padding: const EdgeInsets.symmetric(vertical: 8),
            color: Theme.of(context).colorScheme.surfaceVariant,
            child: Text(
              DateFormat('EEEE, d MMMM yyyy').format(_selectedDate),
              textAlign: TextAlign.center,
              style: const TextStyle(fontWeight: FontWeight.w600),
            ),
          ),
          Expanded(
            child: _loading
                ? const Center(child: CircularProgressIndicator())
                : _error != null
                    ? Center(child: Text('Error: $_error'))
                    : TabBarView(
                        controller: _tabController,
                        children: [
                          _buildList(_gainers, 'No gainers found >= 3% on this date'),
                          _buildList(_losers, 'No losers found >= 3% on this date'),
                        ],
                      ),
          ),
        ],
      ),
    );
  }

  Widget _buildList(List<Mover> movers, String emptyMessage) {
    if (movers.isEmpty) {
      return Center(child: Text(emptyMessage));
    }
    return RefreshIndicator(
      onRefresh: _loadData,
      child: ListView.builder(
        itemCount: movers.length,
        itemBuilder: (context, index) => MoverTile(mover: movers[index]),
      ),
    );
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }
}
