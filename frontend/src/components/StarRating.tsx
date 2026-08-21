export function StarRating({
  value,
  onChange,
}: {
  value: number;
  onChange?: (rating: number) => void;
}) {
  const stars = [1, 2, 3, 4, 5];
  return (
    <div className={`star-rating ${onChange ? "interactive" : ""}`}>
      {stars.map((star) => (
        <span
          key={star}
          className={star <= value ? "star filled" : "star"}
          onClick={onChange ? () => onChange(star) : undefined}
        >
          ★
        </span>
      ))}
    </div>
  );
}
