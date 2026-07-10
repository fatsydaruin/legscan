import 'package:flutter/material.dart';
import '../models/mover.dart';

class MoverTile extends StatelessWidget {
  final Mover mover;

  const MoverTile({super.key, required this.mover});

  @override
  Widget build(BuildContext context) {
    final isGainer = mover.category == 'gainer';
    final color = isGainer ? Colors.green.shade600 : Colors.red.shade600;
    final sign = mover.pctChange > 0 ? '+' : '';

    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      elevation: 1,
      child: ListTile(
        contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        leading: CircleAvatar(
          backgroundColor: color.withOpacity(0.15),
          child: Icon(
            isGainer ? Icons.trending_up : Icons.trending_down,
            color: color,
          ),
        ),
        title: Text(
          mover.symbol,
          style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
        ),
        subtitle: Text(
          'Prev: ₹${mover.prevClose.toStringAsFixed(2)}  →  Close: ₹${mover.closePrice.toStringAsFixed(2)}'
          '${mover.volume != null ? '\nVolume: ${_formatVolume(mover.volume!)}' : ''}',
          style: TextStyle(color: Colors.grey.shade600, fontSize: 12),
        ),
        isThreeLine: mover.volume != null,
        trailing: Text(
          '$sign${mover.pctChange.toStringAsFixed(2)}%',
          style: TextStyle(
            color: color,
            fontWeight: FontWeight.bold,
            fontSize: 16,
          ),
        ),
      ),
    );
  }

  String _formatVolume(int volume) {
    if (volume >= 10000000) return '${(volume / 10000000).toStringAsFixed(1)}Cr';
    if (volume >= 100000) return '${(volume / 100000).toStringAsFixed(1)}L';
    if (volume >= 1000) return '${(volume / 1000).toStringAsFixed(1)}K';
    return volume.toString();
  }
}
