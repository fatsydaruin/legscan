class Mover {
  final String symbol;
  final double closePrice;
  final double prevClose;
  final double pctChange;
  final int? volume;
  final String category; // 'gainer' or 'loser'
  final DateTime tradeDate;

  Mover({
    required this.symbol,
    required this.closePrice,
    required this.prevClose,
    required this.pctChange,
    required this.volume,
    required this.category,
    required this.tradeDate,
  });

  factory Mover.fromJson(Map<String, dynamic> json) {
    return Mover(
      symbol: json['symbol'] as String,
      closePrice: (json['close_price'] as num).toDouble(),
      prevClose: (json['prev_close'] as num).toDouble(),
      pctChange: (json['pct_change'] as num).toDouble(),
      volume: json['volume'] != null ? (json['volume'] as num).toInt() : null,
      category: json['category'] as String,
      tradeDate: DateTime.parse(json['trade_date'] as String),
    );
  }
}
