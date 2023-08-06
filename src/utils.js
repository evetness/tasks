export function formatCurrency(amount, currency) {
  const formatter = new Intl.NumberFormat('hu-HU', {
    style: 'currency',
    currency: currency,
  });
  return formatter.format(amount)
}