import React from 'react';

interface CardProps {
  title?: string;
  children: React.ReactNode;
  className?: string;
  onClick?: () => void;
}

const Card: React.FC<CardProps> = ({
  title,
  children,
  className = '',
  onClick
}) => {
  const baseClasses = 'bg-white rounded-xl shadow-sm border border-gray-100 p-4';
  const clickableClasses = onClick ? 'cursor-pointer hover:shadow-md transition-shadow duration-200' : '';
  
  const classes = `${baseClasses} ${clickableClasses} ${className}`;
  
  return (
    <div className={classes} onClick={onClick}>
      {title && (
        <h3 className="text-lg font-semibold text-gray-900 mb-3">
          {title}
        </h3>
      )}
      {children}
    </div>
  );
};

export default Card;
