x = [0 0 0 1 1];
y = [0 1 0 1 0];
m = 5;
N = 2^m - 1;
gold = zeros(1, N);

%1
fprintf('x: ');
fprintf('%d', x);
fprintf('\n');

fprintf('y: ');
fprintf('%d', y);
fprintf('\n\n');

for i = 1:N
    out = xor(x(5), y(5));
    gold(i) = out;

    xor_x = xor(x(4), x(5));
    xor_y = xor(y(2), y(5));

    x(2:5) = x(1:4);
    y(2:5) = y(1:4);

    % Запись новых битов в начало
    x(1) = xor_x;
    y(1) = xor_y;
end

fprintf('Последовательность Голда:\n');
fprintf('%d', gold);
fprintf('\n\n');

% 2
% Переводим 0/1 в +1/-1 (так принято считать корреляцию)
gold_pm = 2*gold - 1;

R_xcorr = xcorr(gold_pm, 'normalized'); % делает так, чтобы при нулевом сдвиге было ровно 1.
R_xcorr = R_xcorr(N:end); % оставляем лаги 0 ... 30

fprintf('Сдвиг |');
for b = 1:N
    fprintf(' %2d', b);  % номера битов
end
fprintf(' | Автокорреляция\n');

fprintf('------+');
fprintf(repmat('---', 1, N));
fprintf('+---------------\n');

for shift = 0:N-1
    % Циклический сдвиг влево
    shifted = gold([shift+1:end, 1:shift]);
    
    fprintf('%5d |', shift);
    fprintf(' %2d', shifted); % печатаем все биты сдвинутой последовательности
    fprintf(' | %+10.4f\n', R_xcorr(shift+1));
end
%3
x_3 = [0 0 1 0 0];
y_3 = [0 0 1 0 1];
gold_3 = zeros(1, N);
fprintf('x_3: ');
fprintf('%d', x_3);
fprintf('\n');

fprintf('y_3: ');
fprintf('%d', y_3);
fprintf('\n\n');

for i = 1:N
    out_3 = xor(x_3(5), y_3(5));
    gold_3(i) = out_3;

    xor_x_3 = xor(x_3(4), x_3(5));
    xor_y_3 = xor(y_3(2), y_3(5));

    x_3(2:5) = x_3(1:4);
    y_3(2:5) = y_3(1:4);

    % Запись новых битов в начало
    x_3(1) = xor_x_3;
    y_3(1) = xor_y_3;
end

fprintf('Вторая последовательность Голда:\n');
fprintf('%d', gold_3);
fprintf('\n\n');
% 4
% Взаимная корреляция при нулевом сдвиге
c = sum(gold == gold_3);          % количество совпадений
o = N - c;                        % количество несовпадений
R_cross0 = (c - o) / N;

fprintf('Взаимная корреляция (лаг 0): %+.4f\n', R_cross0);
% 6
figure;
stem(0:N-1, R_xcorr, 'filled', 'LineWidth', 1.2);
grid on;
xlabel('Сдвиг (lag)');
ylabel('Автокорреляция R');
title('Автокорреляционная функция последовательности Голда');
ylim([-0.5 1.15]);
xlim([-1 N]);